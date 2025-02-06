import openai


async def call_llm(token: str, model: str, prompt: str):
    client = openai.AsyncOpenAI(api_key=token)

    response = await client.chat.completions.create(
        model=model,
        messages=[{"role": "system", "content": prompt}],
        temperature=0.7,
    )

    return response.choices[0].message["content"]
