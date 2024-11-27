import os

from dotenv import load_dotenv
from mistralai import Mistral

load_dotenv()
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")
client = Mistral(api_key=MISTRAL_API_KEY)

async def get_mistral_answer(
    content,
    model="open-mistral-nemo",
):
    response = await client.chat.stream_async(
        model=model,
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


if __name__ == "__main__":
    prompt = """Determine the sentiment of the following text. Only respond with the exact words "positive" or "negative".

    The film is very impressive! Definitely recommend it."""
    print(get_mistral_answer(prompt))
