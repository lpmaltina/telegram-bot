async def get_mistral_answer(
    client,
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
