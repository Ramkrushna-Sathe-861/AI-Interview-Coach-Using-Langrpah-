from app.prompts.prompts import mock_interview_prompt
from app.services.llm_service import LLMService

class MockInterviewer:
    def __init__(self, llm: LLMService):
        self.llm = llm

    def ask(self, profile: str, target_role: str, history: str) -> dict:
        prompt = mock_interview_prompt.format(
            profile=profile,
            target_role=target_role,
            history=history,
        )
        raw_output = self.llm.complete(prompt)
        return {"mock_interview": raw_output}
