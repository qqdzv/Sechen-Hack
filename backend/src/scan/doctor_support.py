import json
import aiohttp
from src.config import CHAT_BOT_API
from src.logger import logger

async def generate_doctor_report(gender: str, age: int, skin_type: str, diagnosis: str, probability: float, disease_type: str, abcd : str) -> dict:
    url = "https://api.aimlapi.com/chat/completions"
    headers = {
        "Authorization": f"Bearer {CHAT_BOT_API}",
        "Content-Type": "application/json"
    }
    prompt = f"""
    ты медик онколог и дерматолог. Нужно на медицинском языке передать врачу информацию о пациенте. 
    Вот данные пациента:
    - Пол: {gender}
    - Возраст: {age}
    - Тип кожи: {skin_type}
    - Диагноз: {diagnosis}
    - Вероятность: {probability}%
    - Тип заболевания: {disease_type} (доброкачественное/злокачественное)
    - Оценка по алгоритму ABCD: {abcd}
    У пациента следующие показатели, согласно ABCD осмотру пигментированного образования по коже:
    A - Показатель Асимметрии
    B - Формы границы 
    C - Цвет 
    D - Диаметр 
    0 - 0.3: Низкий риск
    0.3 - 0.6: Средний риск
    0.6 - 1.0: Высокий риск

    Составь подробный о диагнозе на основе предоставленных данных, алгоритма ABCD. Отчет должен содержать результат о диагнозе, насколько он опасен  или не опасен,  что оно значит по медицински. какие симптомы , последствия могут быть, какие анализы должен сдать пациент в плохом случае. должно быть на медицинском языке все.
    
    Весь результат выведи в JSON в таком формате:
    
    'result': 'Результат, который будет показан врачу на медицинском языке'
            
    """

    payload = json.dumps({
        "model": "gpt-4o",
        "messages": [
            {
                "role": "user",
                "content": [{"type": "text", "text": prompt}]
            }
        ],
        "max_tokens": 500
    })
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, data=payload) as response:
                response_data = await response.json()
                response_data = (response_data['choices'][0]['message']['content'])[7:-3]
                response_dict = json.loads((response_data))
                return response_dict
    except Exception as err:
        logger.error(err)
        