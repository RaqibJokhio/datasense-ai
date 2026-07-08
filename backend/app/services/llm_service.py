import httpx
from fastapi import HTTPException
from app.core.config import settings

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

SYSTEM_PROMPT = """You are a data analysis code generator. Given a pandas DataFrame called `df` and a user question, write Python code that answers it.

Rules:
- Only use the variable `df` (already loaded), pandas (as pd), and numpy (as np).
- Do NOT import anything, do NOT read/write files, do NOT use exec/eval/os/sys.
- Store the final answer in a variable called `result`.
- If the answer is a chart, use matplotlib (as plt) and save it to a variable called `result` as the matplotlib figure object (plt.gcf()).
- Keep code short and correct. No explanations, no markdown, ONLY raw Python code.
"""

async def generate_pandas_code(question: str, columns: list[str], dtypes: dict[str, str]) -> str:
    schema_info = "\n".join([f"- {col} ({dtypes.get(col, 'unknown')})" for col in columns])

    user_prompt = f"""DataFrame columns:
{schema_info}

Question: {question}

Write the pandas code."""

    payload = {
        "model": settings.OPENROUTER_MODEL,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
        "temperature": 0.1,
    }

    headers = {
        "Authorization": f"Bearer {settings.OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
    }

    async with httpx.AsyncClient(timeout=60.0) as client:
        try:
            response = await client.post(OPENROUTER_URL, json=payload, headers=headers)
        except httpx.TimeoutException:
            raise HTTPException(status_code=504, detail="The AI model took too long to respond. Please try again.")
        except httpx.RequestError:
            raise HTTPException(status_code=503, detail="Could not reach the AI service. Check your internet connection.")

    if response.status_code == 429:
        raise HTTPException(status_code=429, detail="Rate limit reached on the free AI model. Please wait a minute and try again.")

    if response.status_code == 404:
        raise HTTPException(status_code=503, detail="The configured AI model is currently unavailable. Try again later.")

    if response.status_code != 200:
        raise HTTPException(status_code=502, detail=f"AI service returned an error (status {response.status_code}).")

    data = response.json()

    if "choices" not in data or not data["choices"]:
        raise HTTPException(status_code=502, detail="AI service returned an unexpected response format.")

    code = data["choices"][0]["message"]["content"]

    code = code.strip()
    if code.startswith("```"):
        lines = code.split("\n")
        code = "\n".join(lines[1:-1]) if lines[-1].strip() == "```" else "\n".join(lines[1:])

    return code