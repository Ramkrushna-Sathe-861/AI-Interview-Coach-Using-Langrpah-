import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
GROQ_MODEL = os.getenv("GROQ_MODEL", "meta-llama/llama-4-scout-17b-16e-instruct")
GROQ_API_URL = os.getenv("GROQ_API_URL", "https://api.groq.com/v1/llm/chat/completions")
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "groq")
LANGGRAPH_API_KEY = os.getenv("LANGGRAPH_API_KEY", "")

if not OPENAI_API_KEY and not GROQ_API_KEY:
    raise ValueError("Either OPENAI_API_KEY or GROQ_API_KEY is required in .env")
