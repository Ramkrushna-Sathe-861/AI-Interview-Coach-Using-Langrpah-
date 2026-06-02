from app.prompts.prompts import feedback_prompt
from app.services.llm_service import LLMService

class FeedbackGenerator:
    def __init__(self, llm: LLMService):
        self.llm = llm

    def review(self, responses: str, context: str) -> dict:
        prompt = feedback_prompt.format(responses=responses, context=context)
        raw_output = self.llm.complete(prompt)
        return {"feedback": raw_output}
