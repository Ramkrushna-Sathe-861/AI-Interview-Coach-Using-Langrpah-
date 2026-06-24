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

# Try to import the optional Groq SDK; if it's not available we'll fall back
# to the HTTP endpoint implementation below.
Groq = None
try:
    groq_mod = importlib.import_module("groq")
    Groq = getattr(groq_mod, "Groq", None)
except ImportError:
    Groq = None


# Configure OpenAI API key (noop if empty)
openai.api_key = OPENAI_API_KEY


# Module-level defaults (read from config)
_DEFAULT_PROVIDER = (LLM_PROVIDER or "openai").lower()
_DEFAULT_OPENAI_MODEL = OPENAI_MODEL
_DEFAULT_GROQ_MODEL = GROQ_MODEL


def _complete_openai(prompt: str, model: str, temperature: float, max_tokens: int) -> str:
    response = openai.ChatCompletion.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=temperature,
        max_tokens=max_tokens,
    )
    return response.choices[0].message.content.strip()


def _complete_groq(prompt: str, model: str, temperature: float, max_tokens: int) -> str:
    if not GROQ_API_KEY:
        raise ValueError("GROQ_API_KEY is required for Groq provider")

    # If the groq SDK is available prefer it
    if Groq is not None:
        client = Groq(api_key=GROQ_API_KEY)
        completion = client.chat.completions.create(
            model=model,
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

    # Fallback to the public Groq HTTP API
    endpoint = GROQ_API_URL
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": temperature,
        "max_completion_tokens": max_tokens,
        "top_p": 1,
    }

    response = requests.post(endpoint, headers=headers, json=payload, timeout=60)
    response.raise_for_status()
    data = response.json()
    return data["choices"][0]["message"]["content"].strip()


def complete(prompt: str, temperature: float = 0.2, max_tokens: int = 800, provider: Optional[str] = None, model: Optional[str] = None) -> str:
    """Simple function-level interface to generate completions.

    For beginners this is easier to call directly; advanced users can still
    instantiate `LLMService` below if they prefer an object.
    """
    provider = (provider or _DEFAULT_PROVIDER).lower()
    if provider == "groq":
        model = model or _DEFAULT_GROQ_MODEL
        return _complete_groq(prompt, model, temperature, max_tokens)

    # default to openai
    model = model or _DEFAULT_OPENAI_MODEL
    return _complete_openai(prompt, model, temperature, max_tokens)


class LLMService:
    """Lightweight compatibility wrapper that delegates to module functions.

    Keeps the previous `LLMService(...).complete(...)` shape but the
    implementation is function-first and easier to follow for learners.
    """

    def __init__(self, model: Optional[str] = None, provider: Optional[str] = None):
        self.provider = (provider or _DEFAULT_PROVIDER).lower()
        self.model = model

    def complete(self, prompt: str, temperature: float = 0.2, max_tokens: int = 800) -> str:
        return complete(prompt, temperature=temperature, max_tokens=max_tokens, provider=self.provider, model=self.model)
