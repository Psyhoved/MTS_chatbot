class ChatBot:
    def __init__(self):
        self.instruction = """
        Ты - чат-бот на сайте, твоя функция помогать. Отвечай развернуто, вежливо и только на русском языке. 
        Если уместно, то в конце своих ответов можешь задать уточняющий вопрос. 
        Если последний вопрос в запросе не связан с контекстом, то откажись от ответа на него! 
        Не повторяй слово в слово то, что ты уже писал ранее. 
        Отвечай на вопросы про сервис Мобильные сотрудники, МТС Координатор и МТС Трекер.
        Продолжи диалог с пользователем сервисов МТС.  
    """

    def ask_bot(self, context, promt: str):
        dop = ' Ответь на последний вопрос или позитивно поддержи диалог'
        query_engine = context.as_query_engine()
        try:
            response = query_engine.query(self.instruction + promt + dop)
        except Exception as e:
            response = f'К сожалению, не могу ответить на Ваш вопрос. Сервис недоступен: {e}'
            return response

        if not response.response or response.response == 'Empty Response':
            return "Не понял Вашего вопроса. Напишите, пожалуйста, точнее, чтобы Вы хотели узнать."
        else:
            return response.response



