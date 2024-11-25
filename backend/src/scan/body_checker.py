import aiohttp
import json
from src.config import CHAT_BOT_API


async def validate_body_scan(image_base64 : str) -> dict:
    url = "https://api.aimlapi.com/chat/completions"
    headers = {
        "Authorization": f"Bearer {CHAT_BOT_API}",
        "Content-Type": "application/json"
    }
    payload = json.dumps({
    "model": "gpt-4o",
    "messages": [
        {
        "role": "user",
        "content": [
            {"type": "text", "text": """
            You are an advanced image analysis model specialized in detecting human skin areas for a skin cancer detection application. Your task is to determine whether the provided image contains a **close-up** of a skin area that is clearly visible and intended for medical examination. The image should be a focused shot of the skin only, including close-ups of facial areas (e.g., chin, cheeks) if applicable, without showing a full person, profile, or other body parts in context.

            Follow these instructions:
            1. If the image contains a **close-up** of a human skin area (including facial regions like chin or cheeks) with no other body parts, profile views, or irrelevant objects in view, return "True".
            2. If the image shows a person standing in profile, full body, a non-close-up face, or contains irrelevant objects or too much background, return "False". Explain why the image is not suitable, and suggest that the user retakes the photo by focusing on a close-up of a specific skin area.

            Respond with a JSON object in the following format:

            {
                "contains_skin": true or false,
                "description": "Краткое описание, объясняющее ваше решение на русском языке."
            }
            """},
            {
            "type": "image_url",
            "image_url": {
                "url": f"{image_base64}"
            }
            }
        ]
        }
    ],
    "max_tokens": 300
    })
    
    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, data=payload) as response:
            response_data = await response.json()
            data = (response_data['choices'][0]['message']['content'])[7:-3]
            data_dict = json.loads(data)
            return data_dict
