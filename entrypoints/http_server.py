from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from llama_index import StorageContext, load_index_from_storage
from pathlib import Path

from entrypoints.MTS_chatbot_api import ChatBot
from libs.http_actions.responses import ChatBotResponse

app = FastAPI()
root_dir = Path(__file__).parent.parent.absolute()
input_index = Path(root_dir, "index.json")


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Сервис чат-бота для клиентов МТС",
        version="0.0.1",
        description="",
        routes=app.routes,
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi

bot = ChatBot()
storage_context = StorageContext.from_defaults(persist_dir=str(input_index))
# load index
# index = load_index_from_storage(storage_context)


@app.get('/')
async def hello():
    """
    ping - pong
    :return:
    :rtype:
    """
    return {'ok': True}


@app.post('/generate_bot_response', response_model=ChatBotResponse)
async def generate_bot_response(promt: str) -> ChatBotResponse:
    """
    Функция, отправляющая контекст (обучение) и промт (вопрос пользователя) в API chat-gpt и возвращающая ответ.
    :param promt: Запрос пользователя для чат-бота
    :type promt: str
    :return: Ответ чат-бота
    :rtype: ChatBotResponse[str]
    """
    response = ChatBotResponse()
    index = load_index_from_storage(storage_context)
    found = bot.ask_bot(context=index, promt=promt)

    if found is None or len(found) == 0:
        response.MTS_chatbot = 'Не удалось получить ответ на Ваш вопрос :( Попробуйте снова!'
    else:
        response.MTS_chatbot = found

    return response

