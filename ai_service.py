import os
from mistralai import Mistral
from dotenv import load_dotenv

load_dotenv()

class AIService:
    def __init__(self):
        self.api_key = os.getenv("MISTRAL_API_KEY")
        self.model = "mistral-small-2506"
        self.client = Mistral(api_key=self.api_key)

    async def generate_email(self, instruction: str) -> str:
        """
        Generates a professional email based on user instructions.
        """
        system_prompt = "You are a professional email assistant. Write clear, polite and well formatted emails."
        
        try:
            chat_response = await self.client.chat.complete_async(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": instruction},
                ]
            )
            return chat_response.choices[0].message.content
        except Exception as e:
            raise Exception(f"Mistral AI Error: {str(e)}")
