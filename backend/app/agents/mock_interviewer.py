from typing import Dict

from app.prompts.prompts import mock_interview_prompt
from app.services.llm_service import LLMService


class MockInterviewer:
    """Simple interview chat agent that formats a prompt and calls an LLM.

    The class is intentionally small to keep responsibilities clear: prepare
    the prompt and delegate to the provided `LLMService`.
    """

    def __init__(self, llm: LLMService):
        self.llm = llm

    def ask(self, profile: str, target_role: str, history: str) -> Dict[str, str]:
        """Return a dictionary with the LLM's response for the mock interview.

        Args:
            profile: Short string describing the candidate (resume/profile).
            target_role: Target role the candidate is interviewing for.
            history: JSON string or serialized history of previous Q/A.

        Returns:
            A dict containing the key `mock_interview` with the LLM output.
        """
        prompt = mock_interview_prompt.format(profile=profile, target_role=target_role, history=history)
        raw_output = self.llm.complete(prompt)
        return {"mock_interview": raw_output}
