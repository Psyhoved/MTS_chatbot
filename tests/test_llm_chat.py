import pytest
import os
import sys

from langchain_core.messages import HumanMessage, AIMessage
from sqlalchemy import create_engine, MetaData
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import SQLChatMessageHistory
from langchain_core.runnables import RunnableBinding

# Добавьте корневую директорию проекта в sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from libs.llm_chat import (check_question,
                           get_history_aware_retriever, define_llm,
                           define_promt, create_chain, create_chain_no_memory,
                           VEC_STORE_LOAD_PATH, API_KEY, API_BASE, MODEL,
                           MAX_TOKENS, TEMPERATURE)


@pytest.fixture(scope="function")
def setup_test_db():
    # Создаем временную базу данных в файле
    test_db_path = 'sqlite:///test_memory.db'
    engine = create_engine(test_db_path)
    metadata = MetaData()

    metadata.create_all(engine)

    # Создаем объект SQLChatMessageHistory и заполняем его тестовыми данными
    message_history = SQLChatMessageHistory(session_id='test_session', connection=engine)
    message_history.add_message(HumanMessage("Test message 1"))
    message_history.add_message(AIMessage("Test message 2"))

    yield engine

    # Закрываем соединение после завершения теста
    engine.dispose()

    # Удаляем тестовую базу данных
    if os.path.exists('test_memory.db'):
        os.remove('test_memory.db')


def test_check_question():
    assert check_question("Это сообщение содержит слово хуй.") == "оператор"
    assert check_question("Нужна поддержка, пожалуйста.") == "оператор"
    assert check_question("Спасибо за помощь!") == "спасибо"
    assert check_question("Какой у вас режим работы?") == "Какой у вас режим работы?"


def test_get_session_history(setup_test_db):
    session_id = "test_session"
    engine = setup_test_db

    # Используем объект engine вместо строки подключения
    history = SQLChatMessageHistory(session_id=session_id, connection=engine)

    # Проверяем, что объект history является экземпляром SQLChatMessageHistory
    assert isinstance(history, SQLChatMessageHistory)
    assert history.session_id == session_id

    # Получаем сообщения из истории
    messages = history.get_messages()

    # Проверяем, что сообщения соответствуют ожидаемым значениям
    assert len(messages) == 2
    assert messages[0].content == 'Test message 1'
    assert messages[1].content == 'Test message 2'


def test_define_llm():
    llm = define_llm(API_KEY, API_BASE, MODEL, 10, 0)

    assert isinstance(llm, ChatOpenAI)

    if MODEL == "mistralai/mistral-7b-instruct:free":
        assert llm.invoke('Привет!').content == "Привет! Как могу помочь"


def test_get_history_aware_retriever():
    llm = define_llm(API_KEY, API_BASE, MODEL, MAX_TOKENS, TEMPERATURE)

    history_aware_retriever = get_history_aware_retriever(llm, VEC_STORE_LOAD_PATH)
    assert isinstance(history_aware_retriever, RunnableBinding)


def test_define_promt():
    prompt = define_promt()
    assert isinstance(prompt, ChatPromptTemplate)

    prompt_no_memory = define_promt(no_memory=True)
    assert isinstance(prompt_no_memory, ChatPromptTemplate)
    assert "chat_history" not in prompt_no_memory.input_variables


def test_create_chain():
    conversational_rag_chain = create_chain()
    assert isinstance(conversational_rag_chain, RunnableWithMessageHistory)
    assert 'get_session_history' in conversational_rag_chain.__dict__.keys()


def test_create_chain_no_memory():
    chain = create_chain_no_memory()
    assert isinstance(chain, RunnableBinding)
    assert 'get_session_history' not in chain.__dict__.keys()
