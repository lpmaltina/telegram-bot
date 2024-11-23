import os

from dotenv import load_dotenv
from mistralai import Mistral

load_dotenv()
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")


def get_mistral_answer(
        content,
        model="open-mistral-nemo",
        api_key=MISTRAL_API_KEY
):
    client = Mistral(api_key=api_key)

    response = client.chat.complete(
        model=model,
        messages=[
             {
                  "role": "user",
                  "content": content
             },
        ],
    )
    return response.choices[0].message.content


if __name__ == "__main__":
    prompt = """Determine the sentiment of the following text. Only respond with the exact words "positive" or "negative".

    The film is very impressive! Definitely recommend it."""
    print(get_mistral_answer(prompt))
