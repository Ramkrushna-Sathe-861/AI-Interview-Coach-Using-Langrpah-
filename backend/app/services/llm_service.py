from typing import Optional

import importlib
import openai
import requests
from app.config import (
    GROQ_API_KEY,
    GROQ_API_URL,
    GROQ_MODEL,
    LLM_PROVIDER,
    OPENAI_API_KEY,
    OPENAI_MODEL,
)

Groq = None
try:
    groq_mod = importlib.import_module("groq")
    Groq = getattr(groq_mod, "Groq", None)
except ImportError:
    Groq = None

openai.api_key = OPENAI_API_KEY

class LLMService:
    def __init__(self, model: Optional[str] = None, provider: Optional[str] = None):
        self.provider = (provider or LLM_PROVIDER).lower()
        if self.provider == "groq":
            self.model = model or GROQ_MODEL
        else:
            self.model = model or OPENAI_MODEL

    def complete(self, prompt: str, temperature: float = 0.2, max_tokens: int = 800) -> str:
        if self.provider == "groq":
            return self._complete_groq(prompt, temperature, max_tokens)
        return self._complete_openai(prompt, temperature, max_tokens)

    def _complete_openai(self, prompt: str, temperature: float, max_tokens: int) -> str:
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature,
            max_tokens=max_tokens,
        )
        return response.choices[0].message.content.strip()

    def _complete_groq(self, prompt: str, temperature: float, max_tokens: int) -> str:
        if not GROQ_API_KEY:
            raise ValueError("GROQ_API_KEY is required for Groq provider")

        if Groq is not None:
            client = Groq(api_key=GROQ_API_KEY)
            completion = client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=temperature,
                max_completion_tokens=max_tokens,
                top_p=1,
                stream=False,
            )

            choice = completion.choices[0]
            if hasattr(choice, "message"):
                return choice.message.content.strip()
            if hasattr(choice, "delta"):
                return (choice.delta.content or "").strip()
            return str(choice)

        endpoint = GROQ_API_URL
        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": temperature,
            "max_completion_tokens": max_tokens,
            "top_p": 1,
        }

        response = requests.post(endpoint, headers=headers, json=payload, timeout=60)
        response.raise_for_status()
        data = response.json()
        return data["choices"][0]["message"]["content"].strip()
