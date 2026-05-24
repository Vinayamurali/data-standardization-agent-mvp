from openai import OpenAI

from app.config import settings


class OpenAIClient:
    """
    OpenAI client wrapper.

    The rest of the application should not directly call OpenAI.
    """

    def __init__(self):
        if not settings.openai_api_key:
            raise ValueError(
                "OPENAI_API_KEY is not configured. Add it to .env or environment variables."
            )

        self.client = OpenAI(api_key=settings.openai_api_key)
        self.model = settings.openai_model

    def generate_text(self, system_prompt: str, user_prompt: str) -> str:
        response = self.client.responses.create(
            model=self.model,
            input=[
                {
                    "role": "system",
                    "content": system_prompt,
                },
                {
                    "role": "user",
                    "content": user_prompt,
                },
            ],
        )

        return response.output_text