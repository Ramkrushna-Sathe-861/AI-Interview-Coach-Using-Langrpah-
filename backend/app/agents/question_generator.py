from app.prompts.prompts import question_prompt
from app.services.llm_service import LLMService

class QuestionGenerator:
    def __init__(self, llm: LLMService):
        self.llm = llm

    def generate(self, target_role: str, skill_gaps: str) -> dict:
        prompt = question_prompt.format(target_role=target_role, skill_gaps=skill_gaps)
        raw_output = self.llm.complete(prompt)
        return {"questions": raw_output}
