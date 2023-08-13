from pydantic import BaseModel


class ChatBotResponse(BaseModel):
    MTS_chatbot: str = ''
