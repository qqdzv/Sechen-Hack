import json
import aiohttp
from src.config import CHAT_BOT_API
from src.logger import logger

async def generate_user_report(gender: str, age: int, skin_type: str, diagnosis: str, probability: float, disease_type: str) -> dict:
    url = "https://api.aimlapi.com/chat/completions"
    headers = {
        "Authorization": f"Bearer {CHAT_BOT_API}",
        "Content-Type": "application/json"
    }
    prompt = f"""
    На основании следующих данных составьте краткий и понятный текст для пользователя:

    - Пол: {gender}
    - Возраст: {age}
    - Тип кожи: {skin_type}
    - Диагноз: {diagnosis}
    - Вероятность: {probability}%
    - Тип заболевания: {disease_type} (доброкачественное/злокачественное)

    Составь отчет о диагнозе на основе предоставленных данных. Отчет должен содержать результат о диагнозе, насколько он опасен  или не опасен. Также дай рекомендации по уходу за кожей или что делать в случае злокачственной опухоле.
    Пиши только два пункта: Результат и рекомендации по уходу.
    
    Результат выведи в Json в таком формате:
    
    {{
        'result': 'Результат, который будет нести в себе главный смысл',
        'recommendations': 'Рекомендации для пользователя по уходу'
    }}
            
    """

    payload = json.dumps({
        "model": "gpt-4o",
        "messages": [
            {
                "role": "user",
                "content": [{"type": "text", "text": prompt}]
            }
        ],
        "max_tokens": 300
    })
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, data=payload) as response:
                response_data = await response.json()
                response_data = (response_data['choices'][0]['message']['content'])[7:-3]
                response_dict = json.loads(response_data)
                return response_dict
    except Exception as err:
        logger.error(err)
        