import httpx
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
        response = await client.post(OPENROUTER_URL, json=payload, headers=headers)
        response.raise_for_status()
        data = response.json()

    code = data["choices"][0]["message"]["content"]

    # Strip markdown code fences if the model adds them anyway
    code = code.strip()
    if code.startswith("```"):
        lines = code.split("\n")
        code = "\n".join(lines[1:-1]) if lines[-1].strip() == "```" else "\n".join(lines[1:])

    return code