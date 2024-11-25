from langchain_community.chat_models import ChatOpenAI
from langchain.chains.conversation.base import ConversationChain
from langchain.memory import ConversationTokenBufferMemory
from langchain.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain_core.messages import HumanMessage, AIMessage
import warnings
import json
from datetime import timedelta
from src.myredis import redis_fastapi
from src.config import CHAT_BOT_API

warnings.filterwarnings("ignore")

SYSTEM_PROMPT = """You are an AI medical assistant specialized in preliminary skin cancer detection. Your role is to:

1. Gather relevant information about skin changes or concerns
2. Ask specific questions about:
 - Appearance (color, shape, size, border irregularity)
 - Changes over time
 - Associated symptoms
 - Location on body
 - Patient's risk factors
3. Provide preliminary assessment based on ABCDE criteria:
 - Asymmetry
 - Border irregularity
 - Color variation
 - Diameter
 - Evolution

Important Guidelines:
- Always maintain a professional and empathetic tone
- Clearly state you are not replacing medical professionals
- Strongly encourage users to seek professional medical evaluation
- Never make definitive diagnoses
- Focus on education and risk awareness
- Provide reliable skin cancer prevention tips
- If there are any concerning symptoms, emphasize the importance of immediate medical attention
- Use previous conversation context to provide more personalized responses
- Remember patient's risk factors and previous symptoms mentioned

Disclaimer: This is an AI assistant and does not replace professional medical advice. All assessments are preliminary and require confirmation from healthcare professionals."""


class EnhancedSkinCancerDetectionBot:
    def __init__(self, role, user_id):
        self.role = role
        self.user_id = user_id
        self.llm = ChatOpenAI(
            temperature=0.2,
            model_name="gpt-4o-2024-08-06",
            api_key=CHAT_BOT_API,
            base_url="https://api.aimlapi.com"
        )

        self.memory = ConversationTokenBufferMemory(
            llm=self.llm,
            memory_key="chat_summary",
            return_messages=True,
            max_token_limit=15000,
        )

        self.prompt = ChatPromptTemplate.from_messages(
            [
                SystemMessagePromptTemplate.from_template(SYSTEM_PROMPT),
                MessagesPlaceholder(variable_name="chat_summary"),
                HumanMessagePromptTemplate.from_template("{input}"),
            ]
        )

        self.conversation = ConversationChain(
            memory=self.memory, prompt=self.prompt, llm=self.llm, verbose=False
        )


    async def get_response(self, message: str) -> str:
        message = message.strip().lower()
        response = await self.conversation.arun({"input": message})
        await self.save_memory()
        return response
    
    async def save_memory(self):
        """Сохраняет память в Redis с TTL 24ч."""
        messages_to_save = [serialize_message(msg) for msg in self.memory.chat_memory.messages]
        memory_data = json.dumps(messages_to_save)
        await redis_fastapi.setex(f"{self.role}:{self.user_id}:memory", timedelta(hours=24), memory_data)
    
    async def load_memory(self):
        """Загружает память пользователя из Redis."""
        memory_data = await redis_fastapi.get(f"{self.role}:{self.user_id}:memory")
        if memory_data:
            memory_data = (json.loads(memory_data))
            self.memory.chat_memory.messages = [deserialize_message(msg) for msg in memory_data]
        
def serialize_message(message):
    if isinstance(message, HumanMessage) or isinstance(message, AIMessage):
        return {
            "type": message.__class__.__name__,
            "content": message.content,
            "additional_kwargs": message.additional_kwargs,
            "response_metadata": message.response_metadata,
        }
    raise TypeError(f"Unsupported message type: {type(message)}")

def deserialize_message(data):
    if data["type"] == "HumanMessage":
        return HumanMessage(
            content=data["content"],
            additional_kwargs=data["additional_kwargs"],
            response_metadata=data["response_metadata"],
        )
    elif data["type"] == "AIMessage":
        return AIMessage(
            content=data["content"],
            additional_kwargs=data["additional_kwargs"],
            response_metadata=data["response_metadata"],
        )
    raise ValueError(f"Unsupported message type: {data['type']}")

async def get_bot_for_user(role : str, user_id: int) -> EnhancedSkinCancerDetectionBot:
    bot = EnhancedSkinCancerDetectionBot(role=role,user_id=user_id)
    await bot.load_memory()
    return bot