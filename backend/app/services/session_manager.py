"""Session storage and dashboard data assembly."""

from __future__ import annotations

import uuid
from datetime import datetime
from typing import Any

from app.models import ActivityLog, SessionProgress, UserProfile, UserSession
from app.services.agent_orchestrator import get_orchestrator


class SessionManager:
    """Keeps user sessions in memory and exposes dashboard-ready data.

    This is intentionally small and transparent. A database-backed repository
    can replace the dictionaries later without changing the API contract.
    """

    def __init__(self) -> None:
        self.sessions: dict[str, UserSession] = {}
        self.activities: dict[str, list[ActivityLog]] = {}

    def create_session(
        self,
        user_id: str,
        name: str,
        email: str,
        current_role: str,
        target_role: str,
        resume_text: str | None = None,
        experience_years: int = 0,
    ) -> UserSession:
        session_id = str(uuid.uuid4())
        profile = UserProfile(
            user_id=user_id,
            name=name,
            email=email,
            current_role=current_role,
            target_role=target_role,
            experience_years=experience_years,
        )

        profile_text = self._profile_text(profile, resume_text)
        pipeline = get_orchestrator().execute_pipeline(
            user_id=user_id,
            session_id=session_id,
            profile=profile_text,
            target_role=target_role,
            resume_text=resume_text,
            experience_years=experience_years,
        )

        match_score = self._match_score_from_pipeline(pipeline)
        session = UserSession(
            session_id=session_id,
            user_id=user_id,
            profile=profile,
            pipeline=pipeline,
            progress=SessionProgress(
                session_id=session_id,
                user_id=user_id,
                overall_score=match_score,
                questions_practiced=0,
                interviews_taken=0,
                current_streak_days=0,
                learning_progress=0,
            ),
        )

        self.sessions[session_id] = session
        self.activities[session_id] = []

        self.log_activity(
            session_id=session_id,
            user_id=user_id,
            activity_type="session_created",
            title="Interview preparation started",
            description=f"Created a plan for {target_role}.",
        )
        self.log_activity(
            session_id=session_id,
            user_id=user_id,
            activity_type="resume_analyzed",
            title="Profile analyzed",
            description="Resume and profile signals were sent through the agent pipeline.",
        )

        return session

    def get_session(self, session_id: str) -> UserSession | None:
        return self.sessions.get(session_id)

    def update_progress(
        self,
        session_id: str,
        overall_score: float | None = None,
        questions_practiced: int | None = None,
        interviews_taken: int | None = None,
        current_streak_days: int | None = None,
        learning_progress: float | None = None,
    ) -> UserSession | None:
        session = self.get_session(session_id)
        if session is None:
            return None

        updates = {
            "overall_score": overall_score,
            "questions_practiced": questions_practiced,
            "interviews_taken": interviews_taken,
            "current_streak_days": current_streak_days,
            "learning_progress": learning_progress,
        }
        for field_name, value in updates.items():
            if value is not None:
                setattr(session.progress, field_name, value)

        now = datetime.now()
        session.progress.updated_at = now
        session.updated_at = now

        self.log_activity(
            session_id=session_id,
            user_id=session.user_id,
            activity_type="progress_updated",
            title="Progress updated",
            description="Dashboard metrics were refreshed.",
            metadata={key: value for key, value in updates.items() if value is not None},
        )
        return session

    def log_activity(
        self,
        session_id: str,
        user_id: str,
        activity_type: str,
        title: str,
        description: str,
        metadata: dict[str, Any] | None = None,
    ) -> ActivityLog:
        activity = ActivityLog(
            activity_id=str(uuid.uuid4()),
            user_id=user_id,
            activity_type=activity_type,
            title=title,
            description=description,
            metadata=metadata or {},
        )
        self.activities.setdefault(session_id, []).append(activity)
        return activity

    def get_activities(self, session_id: str, limit: int = 10) -> list[ActivityLog]:
        activities = self.activities.get(session_id, [])
        return sorted(activities, key=lambda item: item.timestamp, reverse=True)[:limit]

    def get_dashboard_data(self, session_id: str) -> dict[str, Any] | None:
        session = self.get_session(session_id)
        if session is None:
            return None

        pipeline_steps = self._pipeline_steps(session)
        skill_gap = self._pipeline_result(session, "Skill Gap Agent")
        learning = self._pipeline_result(session, "Learning Agent")
        interview = self._pipeline_result(session, "Interview Agent")

        return {
            "session_id": session_id,
            "user": self._profile_response(session.profile),
            "metrics": self._metrics_response(session.progress),
            "pipeline": pipeline_steps,
            "skills": {
                "strong": skill_gap.get("strong_skills", []),
                "weak": skill_gap.get("missing_skills", []),
                "match_score": skill_gap.get("match_score", 0),
            },
            "learning": learning,
            "interview": interview,
            "activities": [
                activity.model_dump(mode="json")
                for activity in self.get_activities(session_id)
            ],
            "timestamp": datetime.now().isoformat(),
        }

    def _profile_text(self, profile: UserProfile, resume_text: str | None) -> str:
        pieces = [
            profile.name,
            profile.current_role,
            f"{profile.experience_years} years experience",
            resume_text or "",
        ]
        return ". ".join(piece for piece in pieces if piece)

    def _match_score_from_pipeline(self, pipeline) -> float:
        for step in pipeline.steps:
            if step.agent_name == "Skill Gap Agent" and step.result:
                return float(step.result.get("match_score", 0))
        return 0

    def _pipeline_steps(self, session: UserSession) -> list[dict[str, Any]]:
        if session.pipeline is None:
            return []

        return [
            {
                "step_number": step.step_number,
                "agent_name": step.agent_name,
                "agent_title": step.agent_title,
                "description": step.description,
                "status": step.status.value,
                "result": step.result,
            }
            for step in session.pipeline.steps
        ]

    def _pipeline_result(self, session: UserSession, agent_name: str) -> dict[str, Any]:
        if session.pipeline is None:
            return {}

        for step in session.pipeline.steps:
            if step.agent_name == agent_name:
                return step.result or {}
        return {}

    def _profile_response(self, profile: UserProfile) -> dict[str, Any]:
        return {
            "user_id": profile.user_id,
            "name": profile.name,
            "email": profile.email,
            "current_role": profile.current_role,
            "target_role": profile.target_role,
            "experience_years": profile.experience_years,
        }

    def _metrics_response(self, progress: SessionProgress) -> dict[str, Any]:
        return {
            "overall_score": progress.overall_score,
            "questions_practiced": progress.questions_practiced,
            "interviews_taken": progress.interviews_taken,
            "current_streak_days": progress.current_streak_days,
            "learning_progress": progress.learning_progress,
            "updated_at": progress.updated_at.isoformat(),
        }


_session_manager: SessionManager | None = None


def get_session_manager() -> SessionManager:
    """Return the shared in-memory session manager."""

    global _session_manager
    if _session_manager is None:
        _session_manager = SessionManager()
    return _session_manager
