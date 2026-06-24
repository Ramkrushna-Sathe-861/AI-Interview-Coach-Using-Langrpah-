"""Readable orchestration for the InterviewPilot agent pipeline."""

from __future__ import annotations

import uuid
from typing import Any

from app.models import AgentPipeline, AgentPipelineStep, AgentStatus


PIPELINE_BLUEPRINT = [
    {
        "agent_name": "Resume Agent",
        "description": "Extracts skills, role history, and experience signals.",
    },
    {
        "agent_name": "Skill Gap Agent",
        "description": "Compares the profile with the target role.",
    },
    {
        "agent_name": "Learning Agent",
        "description": "Builds a practical roadmap from the missing skills.",
    },
    {
        "agent_name": "Interview Agent",
        "description": "Prepares adaptive mock interview questions.",
    },
    {
        "agent_name": "Feedback Agent",
        "description": "Reviews answers and turns them into next steps.",
    },
]


class AgentOrchestrator:
    """Runs the five backend agents in a predictable, easy-to-read order."""

    def execute_pipeline(
        self,
        user_id: str,
        session_id: str,
        profile: str,
        target_role: str,
        resume_text: str | None = None,
        experience_years: int = 0,
    ) -> AgentPipeline:
        """Create one pipeline run and attach each agent's result."""

        resume_result = self._resume_agent(
            profile=profile,
            resume_text=resume_text,
            experience_years=experience_years,
        )
        skill_gap_result = self._skill_gap_agent(
            resume_result=resume_result,
            target_role=target_role,
        )
        learning_result = self._learning_agent(
            skill_gap_result=skill_gap_result,
            target_role=target_role,
        )
        interview_result = self._interview_agent(
            target_role=target_role,
            skill_gap_result=skill_gap_result,
        )

        steps = [
            self._step(1, AgentStatus.COMPLETED, resume_result),
            self._step(2, AgentStatus.COMPLETED, skill_gap_result),
            self._step(3, AgentStatus.COMPLETED, learning_result),
            self._step(4, AgentStatus.IN_PROGRESS, interview_result),
            self._step(5, AgentStatus.PENDING, None),
        ]

        return AgentPipeline(
            pipeline_id=str(uuid.uuid4()),
            session_id=session_id,
            user_id=user_id,
            steps=steps,
        )

    def _step(
        self,
        step_number: int,
        status: AgentStatus,
        result: dict[str, Any] | None,
    ) -> AgentPipelineStep:
        blueprint = PIPELINE_BLUEPRINT[step_number - 1]
        agent_name = blueprint["agent_name"]
        return AgentPipelineStep(
            step_number=step_number,
            agent_name=agent_name,
            agent_title=agent_name,
            description=blueprint["description"],
            status=status,
            result=result,
        )

    def _resume_agent(
        self,
        profile: str,
        resume_text: str | None,
        experience_years: int,
    ) -> dict[str, Any]:
        """Extract a lightweight candidate summary from profile text."""

        text = " ".join(part for part in [profile, resume_text or ""] if part)
        skills = self._extract_known_skills(text)

        return {
            "summary": profile or "Candidate profile not provided.",
            "experience_years": experience_years,
            "extracted_skills": skills,
            "resume_received": bool(resume_text),
        }

    def _skill_gap_agent(
        self,
        resume_result: dict[str, Any],
        target_role: str,
    ) -> dict[str, Any]:
        """Compare extracted skills against common backend-role needs."""

        target_skills = self._target_skills_for(target_role)
        extracted = {
            skill["name"].lower(): skill
            for skill in resume_result.get("extracted_skills", [])
        }

        strong_skills = []
        missing_skills = []
        for skill_name in target_skills:
            existing = extracted.get(skill_name.lower())
            if existing:
                strong_skills.append(existing)
            else:
                missing_skills.append(
                    {"name": skill_name, "proficiency": 35, "category": "growth"}
                )

        match_score = round((len(strong_skills) / len(target_skills)) * 100)

        return {
            "target_role": target_role,
            "match_score": match_score,
            "strong_skills": strong_skills,
            "missing_skills": missing_skills,
            "strong_skills_count": len(strong_skills),
            "missing_skills_count": len(missing_skills),
            "matched_skills_count": len(strong_skills),
        }

    def _learning_agent(
        self,
        skill_gap_result: dict[str, Any],
        target_role: str,
    ) -> dict[str, Any]:
        """Turn missing skills into a compact learning roadmap."""

        modules = []
        for skill in skill_gap_result.get("missing_skills", [])[:4]:
            skill_name = skill["name"]
            modules.append(
                {
                    "skill": skill_name,
                    "title": f"{skill_name} for {target_role}",
                    "estimated_hours": 8,
                    "difficulty": "medium",
                }
            )

        return {
            "target_role": target_role,
            "modules": modules,
            "total_estimated_hours": sum(module["estimated_hours"] for module in modules),
            "estimated_weeks": max(1, len(modules)),
        }

    def _interview_agent(
        self,
        target_role: str,
        skill_gap_result: dict[str, Any],
    ) -> dict[str, Any]:
        """Generate interview prompts from the target role and weak areas."""

        weak_areas = [
            skill["name"] for skill in skill_gap_result.get("missing_skills", [])
        ] or ["system design", "project experience", "debugging"]

        questions = [
            {
                "id": str(uuid.uuid4()),
                "question": f"How would you explain your experience with {weak_areas[0]}?",
                "category": "skill_gap",
                "difficulty": "medium",
            },
            {
                "id": str(uuid.uuid4()),
                "question": f"Design a production-ready service for a {target_role} team.",
                "category": "system_design",
                "difficulty": "hard",
            },
            {
                "id": str(uuid.uuid4()),
                "question": "Tell me about a technical decision you made and its tradeoffs.",
                "category": "behavioral",
                "difficulty": "medium",
            },
        ]

        return {
            "target_role": target_role,
            "questions": questions,
            "interview_type": "technical",
            "estimated_duration_minutes": 45,
        }

    def _extract_known_skills(self, text: str) -> list[dict[str, Any]]:
        known_skills = [
            ("Python", "language"),
            ("FastAPI", "framework"),
            ("React", "frontend"),
            ("TypeScript", "language"),
            ("SQL", "database"),
            ("Docker", "devops"),
            ("Kubernetes", "devops"),
            ("AWS", "cloud"),
            ("CI/CD", "devops"),
            ("System Design", "architecture"),
            ("LangGraph", "ai"),
        ]

        normalized_text = text.lower()
        skills = []
        for name, category in known_skills:
            if name.lower() in normalized_text:
                skills.append(
                    {"name": name, "proficiency": 80, "category": category}
                )

        if skills:
            return skills

        return [
            {"name": "Python", "proficiency": 70, "category": "language"},
            {"name": "Communication", "proficiency": 75, "category": "soft_skill"},
        ]

    def _target_skills_for(self, target_role: str) -> list[str]:
        role = target_role.lower()
        if "frontend" in role:
            return ["React", "TypeScript", "System Design", "Communication"]
        if "ai" in role or "ml" in role:
            return ["Python", "LangGraph", "System Design", "SQL", "AWS"]
        return ["Python", "FastAPI", "SQL", "Docker", "AWS", "System Design"]


_orchestrator: AgentOrchestrator | None = None


def get_orchestrator() -> AgentOrchestrator:
    """Return the shared orchestrator instance."""

    global _orchestrator
    if _orchestrator is None:
        _orchestrator = AgentOrchestrator()
    return _orchestrator
