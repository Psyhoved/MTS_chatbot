from pydantic import BaseModel


class BotRequest(BaseModel):
    prompt: str = ''
