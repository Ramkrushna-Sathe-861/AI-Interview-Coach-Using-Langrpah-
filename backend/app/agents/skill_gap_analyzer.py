from app.prompts.prompts import skill_gap_prompt
from app.services.llm_service import LLMService

class SkillGapAnalyzer:
    def __init__(self, llm: LLMService):
        self.llm = llm

    def analyze(self, skills: str, experience_summary: str, target_role: str) -> dict:
        prompt = skill_gap_prompt.format(
            skills=skills,
            experience_summary=experience_summary,
            target_role=target_role,
        )
        raw_output = self.llm.complete(prompt)
        return {"skill_gap_analysis": raw_output}
