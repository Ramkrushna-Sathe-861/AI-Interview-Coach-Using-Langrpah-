from app.prompts.prompts import resume_analysis_prompt
from app.services.llm_service import LLMService

class ResumeAnalyzer:
    def __init__(self, llm: LLMService):
        self.llm = llm

    def analyze(self, resume_text: str) -> dict:
        prompt = resume_analysis_prompt.format(resume_text=resume_text)
        raw_output = self.llm.complete(prompt)
        return {
            "resume_text": resume_text,
            "analysis": raw_output,
        }
