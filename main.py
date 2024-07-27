from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from libs.llm_chat import create_chain, check_question

# Создание экземпляра FastAPI
app = FastAPI()


# Модель данных для запроса
class QuestionRequest(BaseModel):
    user_id: str
    question: str


# инициализация чат-бота
chain = create_chain()


@app.post("/ask")
async def ask_question(request: QuestionRequest):
    user_id = request.user_id
    question = check_question(request.question)
    if question == 'оператор':
        return JSONResponse(content={"response": 'Перевожу на оператора...'})
    elif question == 'спасибо':
        return JSONResponse(content={"response": 'Всегда готовы помочь! Желаем Вам всего самого доброго! 💚'})

    # Отправка запроса модели
    try:

        response_content = chain.invoke({"input": question}, config={"configurable": {"session_id": user_id}})['answer']

        return JSONResponse(content={"response": response_content})

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
