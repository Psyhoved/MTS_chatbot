from langchain_core.runnables import RunnableBinding
from langchain_openai import ChatOpenAI
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.chains import create_retrieval_chain, create_history_aware_retriever

from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import SQLChatMessageHistory

import re
import os
from dotenv import load_dotenv
from pathlib import Path

from vectorstore import load_vectorstore

load_dotenv()

# Определение корневого каталога проекта
PROJECT_ROOT = Path(__file__).parent.parent.absolute()
VEC_STORE_LOAD_PATH = Path.joinpath(PROJECT_ROOT, "faik_FAISS_store.db")
USER_STORY_BD_PATH = Path.joinpath(PROJECT_ROOT, 'user_story_bd.pickle')
API_KEY = os.environ.get("OPEN_ROUTER_KEY")
API_BASE = "https://openrouter.ai/api/v1"
MODEL = "mistralai/mistral-7b-instruct:free"
MAX_TOKENS = 500
TEMPERATURE = 0.5


def check_question(message: str) -> str:
    """
    Проверяет сообщение на наличие матерных слов, запросов к оператору и благодарностей.

    Args:
        message (str): Входящее сообщение пользователя.

    Returns:
        str: "оператор" если обнаружены матерные слова или запрос к оператору,
         "спасибо" если сообщение является благодарностью, иначе возвращает исходное сообщение.
    """

    # Примерный список матерных слов на русском языке (закройте ушки)
    curse_words = [
        'хуй', 'пизда', 'ебать', 'ебаный', 'блядь', 'сука', 'пидор', 'гондон', 'мудак', 'сука', 'мразь', 'говно',
        'дерьмо', 'охуел', 'ебанулся', 'дурак', 'заебал'
    ]

    # Расширенный список слов для вызова оператора
    operator_words = [
        'оператор', 'поддержка', 'help', 'support', 'позови', 'assistance', 'customer service', 'саппорт', 'свяжите',
        'соедините'
    ]

    thanks_words = [
        'спасибо', "благодарю", "спасибо за помощь", "благодарствую", "чао", "пока", "досвидания", "до свидания"
    ]

    # Приводим сообщение к нижнему регистру для унификации поиска
    message_lower = message.lower()

    # Проверяем на наличие матерных слов
    for curse_word in curse_words:
        if re.search(r'\b' + re.escape(curse_word) + r'\b', message_lower):
            return "оператор"

    # Проверяем на наличие слов для обращения к оператору
    for operator_word in operator_words:
        if re.search(r'\b' + re.escape(operator_word) + r'\b', message_lower):
            return "оператор"

    # Проверяем на окончание диалога
    for thanks_word in thanks_words:
        if re.search(r'\b' + re.escape(thanks_word) + r'\b', message_lower):
            return "спасибо"

    return message


def get_session_history(session_id: str, conn_str2db: str = "sqlite:///memory.db") -> BaseChatMessageHistory:
    """
    Возвращает историю сообщений для заданной сессии.

    Args:
        session_id (str): Идентификатор сессии.
        conn_str2db (str, optional): Строка подключения к базе данных. По умолчанию "sqlite:///memory.db".

    Returns:
        BaseChatMessageHistory: Объект истории сообщений чата.
    """

    return SQLChatMessageHistory(session_id, conn_str2db)


def get_history_aware_retriever(llm: ChatOpenAI, vec_store_path: str | Path = VEC_STORE_LOAD_PATH) -> RunnableBinding:
    """
    Создает и возвращает ретривер, учитывающий историю чата.

    Args:
        llm (ChatOpenAI): Языковая модель.
        vec_store_path(str): путь к векторному хранилищу базы знаний
    Returns:
        HistoryAwareRetriever: Ретривер, который учитывает историю чата.
    """

    retriever = load_vectorstore(vec_store_path).as_retriever()

    contextualize_q_system_prompt = """Учитывая историю чата и последний вопрос пользователя, \
    который может ссылаться на контекст в истории чата, сформулируй отдельный вопрос, \
    который можно понять без истории чата. НЕ ОТВЕЧАЙ на вопрос, просто переформулируйте его, \
    если необходимо, и в противном случае верните его как есть.
    """

    contextualize_q_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", contextualize_q_system_prompt),
            MessagesPlaceholder("chat_history"),
            ("human", "{input}"),
        ]
    )

    history_aware_retriever = create_history_aware_retriever(
        llm, retriever, contextualize_q_prompt
    )

    return history_aware_retriever


def define_llm(api_key: str, api_base: str, model: str, max_tokens: int, temperature: float) -> ChatOpenAI:
    """
        Определяет и возвращает языковую модель.

    Args:
        api_key (str): API ключ для доступа к модели.
        api_base (str): Базовый URL для доступа к API.
        model (str): Имя модели.
        max_tokens (int): Максимальное количество токенов для генерации.
        temperature (float): Температура генерации текста.

    Returns:
        ChatOpenAI: Языковая модель.
    """

    llm = ChatOpenAI(openai_api_key=api_key,
                     openai_api_base=api_base,
                     model_name=model,
                     max_tokens=max_tokens,
                     temperature=temperature)
    return llm


def define_promt(no_memory: bool = False) -> ChatPromptTemplate:
    """
    Определяет и возвращает системный промт.

    Args:
        no_memory (bool, optional): Указывает, использовать ли историю сообщений. По умолчанию False.

    Returns:
        ChatPromptTemplate: Системный промт.
    """
    system_prompt = """ Ты - чат-бот Енот, и работаешь в чате сети магазинов хороших продуктов "Жизньмарт",
    твоя функция - стараться ответить на любой вопрос клиента про работу магазинов "Жизьмарт".
    Используй в ответах только русский язык! Не отвечай на английском! 
    Если вопрос не касается контекста, то вежливо и дружелюбно переведи тему и расскажи про Живчики Жизьмарта.

    {context}

    Используй только этот контекст, чтобы ответить на последний вопрос.
    Если ответа нет в контексте, просто позитивно поддержи диалог на тему Жизньмарта!
    Если клиент поздоровался с тобой, но НЕ ЗАДАЛ вопрос, тогда поздоровайся и спроси, чем ему помочь!
    """
    # Если клиент доволен ответом на вопрос, например, говорит "спасибо", скажи "спасибо" и попрощайся.

    if no_memory:
        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", system_prompt),
                ("human", "{input}"),
            ]
        )
    else:
        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", system_prompt),
                MessagesPlaceholder("chat_history"),
                ("human", "{input}"),
            ]
        )

    return prompt


def create_chain() -> RunnableWithMessageHistory:
    """
        Создает и возвращает цепочку обработки запросов с учетом истории чата.

    Returns:
        RunnableWithMessageHistory: Цепочка обработки запросов с учетом истории чата.
    """
    llm = define_llm(API_KEY, API_BASE, MODEL, MAX_TOKENS, TEMPERATURE)
    prompt = define_promt()

    doc_chain = create_stuff_documents_chain(llm, prompt)
    history_aware_retriever = get_history_aware_retriever(llm)

    chain = create_retrieval_chain(history_aware_retriever, doc_chain)

    # Create a chain
    conversational_rag_chain = RunnableWithMessageHistory(
        chain,
        get_session_history,
        input_messages_key="input",
        history_messages_key="chat_history",
        output_messages_key="answer",
    )

    return conversational_rag_chain


def create_chain_no_memory():
    """
    Создает и возвращает цепочку обработки запросов без учета истории чата.

    Returns:
        RetrievalChain: Цепочка обработки запросов без учета истории чата.
    """

    llm = define_llm(API_KEY, API_BASE, MODEL, MAX_TOKENS, TEMPERATURE)
    prompt = define_promt(no_memory=True)
    retriever = load_vectorstore(VEC_STORE_LOAD_PATH).as_retriever()

    doc_chain = create_stuff_documents_chain(llm, prompt)
    # Create a chain
    chain = create_retrieval_chain(retriever, doc_chain)

    return chain
