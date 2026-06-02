from app.prompts.prompts import roadmap_prompt
from app.services.llm_service import LLMService

class RoadmapGenerator:
    def __init__(self, llm: LLMService):
        self.llm = llm

    def generate(self, profile: str, target_role: str) -> dict:
        prompt = roadmap_prompt.format(profile=profile, target_role=target_role)
        raw_output = self.llm.complete(prompt)
        return {"roadmap": raw_output}
