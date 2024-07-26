import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from openai import OpenAI

load_dotenv()

# Инициализация клиента OpenAI
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.environ.get("OPEN_ROUTER_KEY"),
)
model = "mistralai/mistral-7b-instruct:free"

# Создание экземпляра FastAPI
app = FastAPI()

# Словарь для хранения истории сообщений пользователей
user_histories = {}


# Модель данных для запроса
class QuestionRequest(BaseModel):
    user_id: int
    question: str

instruction = ("""Ты - чат-бот Енот, и работаешь в чате сети магазинов хороших продуктов "Жизньмарт",
     твоя функция - стараться ответить на любой вопрос клиента про работу магазинов "Жизьмарт".  
     Используй в ответах только русский язык! Не отвечай на английском!
     Если вопрос не касается контекста, то вежливо и дружелюбно переведи тему и расскажи про Живчики Жизьмарта
     """)

# Системный промт
system_prompt = {
    "role": "system",
    "content": instruction,
}

@app.post("/ask")
async def ask_question(request: QuestionRequest):
    user_id = request.user_id
    question = request.question

    # Получаем историю сообщений пользователя
    if user_id not in user_histories:
        user_histories[user_id] = [system_prompt]

    user_histories[user_id].append({"role": "user", "content": question + '\n Ответь на последний вопрос или позитивно поддержи диалог'})

    # Отправка запроса модели
    try:
        response = client.chat.completions.create(
            model=model,
            messages=user_histories[user_id],
            max_tokens=500,
            temperature=1
        )

        response_content = response.choices[0].message.content

        user_histories[user_id].append({"role": "assistant", "content": response_content})

        return JSONResponse(content={"response": response_content})

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
