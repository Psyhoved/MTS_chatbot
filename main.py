import os

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from langchain_core.messages import HumanMessage, AIMessage

from libs.llm_chat import create_chain, check_question, create_chain_no_memory, get_session_history

description = """
## Версии
### 0.0.1
- Добавлен перевод на оператора при запросе.
- Добавлен ответ "спасибо" при завершении диалога.
### 0.0.2
- Добавлена модель без учёта истории общения с пользователем (для тестов).
### 0.0.3
- Добавлено сохранение истории диалогов в базу данных SQLlite.
- Исправлен баг с неадекватным ответом на приветствие
- Увеличено покрытия кода тестами
"""

# Создание экземпляра FastAPI
app = FastAPI(
    title="Чат-бот API Жизньмарт",
    version="0.0.3",
    description=description)


# Модель данных для запроса
class QuestionRequest(BaseModel):
    user_id: str
    question: str


class HistoryRequest(BaseModel):
    user_id: str


# проверка наличия векторстора с базой знаний
bk_path = "База знаний фейк.pdf"
vec_store_save_path = "faik_FAISS_store.db"

if not os.path.exists(vec_store_save_path):
    from vectorstore import make_vectorstore
    make_vectorstore(bk_path, vec_store_save_path)

del bk_path, vec_store_save_path

# инициализация чат-бота
chain = create_chain()
chain_no_memory = create_chain_no_memory()


@app.post("/ask_mistral_7b_instruct")
async def ask_mistral_7b_instruct(request: QuestionRequest):
    """
    Общение с ботом с учётом истории сообщений с пользователем. В промт идёт вся прошлая переписка.

    :param request:

    :return:
    """
    user_id = request.user_id
    question = check_question(request.question)
    if question == 'оператор':
        return JSONResponse(content={"response": 'Перевожу на оператора...'})
    elif question == 'спасибо':
        return JSONResponse(content={"response": 'Всегда готовы помочь! Желаем Вам всего самого доброго! 💚'})

    # Отправка запроса модели
    try:

        response_content = chain.invoke({"input": question}, config={"configurable": {"session_id": user_id}})

        return JSONResponse(content={"response": response_content['answer']})

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/ask_mistral_7b_instruct_no_memory")
async def ask_mistral_7b_instruct_no_memory(request: QuestionRequest):
    """
    Общение с ботом без учёта истории сообщений с пользователем. Каждый вопрос, как первый.

    :param request:

    :return:
    """
    question = check_question(request.question)
    if question == 'оператор':
        return JSONResponse(content={"response": 'Перевожу на оператора...'})
    elif question == 'спасибо':
        return JSONResponse(content={"response": 'Всегда готовы помочь! Желаем Вам всего самого доброго! 💚'})

    # Отправка запроса модели
    try:

        response_content = chain_no_memory.invoke({"input": question})['answer']

        return JSONResponse(content={"response": response_content})

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/get_history")
async def get_history(request: HistoryRequest):
    user_id = request.user_id
    session_history = get_session_history(user_id)

    # Преобразование сообщений в список словарей
    messages = []
    for message in session_history.get_messages():
        if isinstance(message, HumanMessage):
            messages.append({"Human": message.content})
        elif isinstance(message, AIMessage):
            messages.append({"AI": message.content})

    return JSONResponse(content={'user_id': user_id, "response": messages})


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
