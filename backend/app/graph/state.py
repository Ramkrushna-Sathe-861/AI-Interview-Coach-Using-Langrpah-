from dataclasses import dataclass, field
from typing import List

@dataclass
class InterviewSession:
    session_id: str
    resume_text: str = ""
    profile: str = ""
    target_role: str = ""
    resume_analysis: dict = field(default_factory=dict)
    skill_gap_analysis: dict = field(default_factory=dict)
    roadmap: dict = field(default_factory=dict)
    questions: dict = field(default_factory=dict)
    history: List[dict] = field(default_factory=list)
    feedback: dict = field(default_factory=dict)
