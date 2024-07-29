from langchain_openai import ChatOpenAI
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.chains import create_retrieval_chain, create_history_aware_retriever

from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

import json
import re
import os
from dotenv import load_dotenv

from vectorstore import load_vectorstore

load_dotenv()

VEC_STORE_LOAD_PATH = "faik_FAISS_store.db"
USER_STORY_BD_PATH = 'user_story_bd.json'
API_KEY = os.environ.get("OPEN_ROUTER_KEY")
API_BASE = "https://openrouter.ai/api/v1"
MODEL = "mistralai/mistral-7b-instruct:free"
MAX_TOKENS = 500
TEMPERATURE = 0.5


def check_question(message: str) -> str:
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


def load_store(store_path: str):
    if not os.path.exists(store_path):
        with open(store_path, 'w') as f:
            json.dump({}, f)

    with open(store_path, 'r') as f:
        store = json.load(f)
    return store


def save_store(store: dict):
    with open(USER_STORY_BD_PATH, 'w') as f:
        json.dump(store, f)


def get_session_history(session_id: str) -> BaseChatMessageHistory:
    store = load_store(USER_STORY_BD_PATH)
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    save_store(store)
    return store[session_id]


def get_history_aware_retriever(llm: ChatOpenAI):
    retriever = load_vectorstore(VEC_STORE_LOAD_PATH).as_retriever()

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
    llm = ChatOpenAI(openai_api_key=api_key,
                     openai_api_base=api_base,
                     model_name=model,
                     max_tokens=max_tokens,
                     temperature=temperature)
    return llm


def define_promt(no_memory: bool = False) -> ChatPromptTemplate:
    system_prompt = """ Ты - чат-бот Енот, и работаешь в чате сети магазинов хороших продуктов "Жизньмарт",
    твоя функция - стараться ответить на любой вопрос клиента про работу магазинов "Жизьмарт".
    Используй в ответах только русский язык! Не отвечай на английском! Не используй слишком много смайликов.
    Если вопрос не касается контекста, то вежливо и дружелюбно переведи тему и расскажи про Живчики Жизьмарта.

    {context}

    Используй только этот контекст, чтобы ответить на последний вопрос.
    Если ответа нет в контексте, просто позитивно поддержи диалог на тему Жизньмарта!
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


def create_chain():
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
    llm = define_llm(API_KEY, API_BASE, MODEL, MAX_TOKENS, TEMPERATURE)
    prompt = define_promt(no_memory=True)
    retriever = load_vectorstore(VEC_STORE_LOAD_PATH).as_retriever()

    doc_chain = create_stuff_documents_chain(llm, prompt)
    # Create a chain
    chain = create_retrieval_chain(retriever, doc_chain)

    return chain
