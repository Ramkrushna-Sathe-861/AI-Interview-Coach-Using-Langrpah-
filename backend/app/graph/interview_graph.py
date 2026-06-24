from typing import Optional, Dict

from app.agents.mock_interviewer import MockInterviewer
from app.services.llm_service import LLMService


# Lazy, function-based singletons for the LLM service and MockInterviewer.
# This avoids module-level side effects at import time and keeps initialization
# under explicit control while still reusing instances across calls.
_llm_service: Optional[LLMService] = None
_mock_interviewer: Optional[MockInterviewer] = None


def get_llm_service() -> LLMService:
    """Return a shared LLMService instance, creating it on first use.

    Using a lazy accessor keeps import-time work minimal and makes tests
    easier because callers can patch `get_llm_service`.
    """
    global _llm_service
    if _llm_service is None:
        _llm_service = LLMService()
    return _llm_service


def get_mock_interviewer() -> MockInterviewer:
    """Return a shared MockInterviewer instance, creating it on first use."""
    global _mock_interviewer
    if _mock_interviewer is None:
        _mock_interviewer = MockInterviewer(get_llm_service())
    return _mock_interviewer


def ask_chat(profile: str, target_role: str, history: str) -> Dict[str, str]:
    """Function-level wrapper that delegates to the MockInterviewer agent.

    Uses lazy accessors so initialization happens on demand and returns a
    simple serializable dictionary suitable for JSON responses.
    """
    return get_mock_interviewer().ask(profile, target_role, history)
