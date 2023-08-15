import logging
import re
import urllib.parse

# Настройка логгера
logging.basicConfig(filename='app.log', level=logging.INFO,
                    format='%(asctime)s - %(message)s')


def check_russian(text: str) -> bool:
    return bool(re.search('[а-яА-Я]', text))


class ChatBot:
    def __init__(self):
        self.instruction = """
        Ты - чат-бот Светлана и работаешь на сайте МТС "Мобильные сотрудники",
        твоя функция - стараться ответить на любой вопрос клиента. 
        Отвечай весело, позитивно, можешь шутить. 
        Используй в ответах только русский язык! Не отвечай на английском! 
        Если вопрос не касается контекста, то вежливо и дружелюбно переведи тему, 
        и расскажи про сервис Мобильные сотрудники, МТС Координатор и МТС Трекер! 
        Отвечай на вопросы про сервис Мобильные сотрудники, МТС Координатор и МТС Трекер.\n  
    """

    def ask_bot(self, context, promt: str):
        dop = ' Ответь на последний вопрос или позитивно поддержи диалог'
        query_engine = context.as_query_engine()
        promt = urllib.parse.unquote(promt)
        logging.info(f"То, что приходит: {promt}")
        try:
            response = query_engine.query(self.instruction + promt + dop)
        except Exception as e:
            response = f'К сожалению, не могу ответить на Ваш вопрос. Сервис недоступен: {e}'
            return response

        if not response.response or response.response == 'Empty Response':
            return "Не понял Вашего вопроса. Напишите, пожалуйста, точнее, чтобы Вы хотели узнать."
        elif not check_russian(response.response):
            response = query_engine.query(response.response + ' Переведи на русский')

        return response.response



