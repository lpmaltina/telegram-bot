import os

from dotenv import load_dotenv

from mistralai import Mistral

load_dotenv()


class MistralModel:
    def __init__(self, model="open-mistral-nemo"):
        self._model = model
        self._mistral_api_key = os.getenv("MISTRAL_API_KEY")
        self._client = Mistral(api_key=self._mistral_api_key)

    async def get_answer(self, content):
        response = await self._client.chat.stream_async(
            model=self._model,
            messages=[
                 {
                      "role": "user",
                      "content": content
                 },
            ],
        )
        text = []
        async for chunk in response:
            if chunk.data.choices[0].delta.content is not None:
                text.append(chunk.data.choices[0].delta.content)
        return "".join(text)
