class ChatBot:
    def __init__(self):
        self.instruction = """Ты - чат-бот на сайте, твоя функция помогать. Отвечай развернуто, вежливо. Если уместно,
    то в конце своих ответов можешь задать уточняющий вопрос. Используй в ответах только русский язык! 
    Если нужно переводи на русский язык с других языков. Не отвечай на английском!
    Если последний вопрос в запросе абсолютно не касается предоставленного контекста, 
    то вежливо и  дружелюбно переведи тему и расскажи про сервис Мобильные сотрудники, МТС Координатор и МТС Трекер!
    Отвечай на вопросы про сервис Мобильные сотрудники, МТС Координатор и МТС Трекер. 
    """

    def ask_bot(self, context, promt: str):
        query_engine = context.as_query_engine()
        try:
            response = query_engine.query(self.instruction + promt)
        except Exception as e:
            response = f'К сожалению, не могу ответить на Ваш вопрос. Сервис недоступен: {e}'
            return response

        if not response.response or response.response == 'Empty Response':
            return "Не понял Вашего вопроса. Напишите, пожалуйста, точнее, чтобы Вы хотели узнать."
        else:
            # self.instruction = promt + ' ' + response.response + ' '
            return response.response



