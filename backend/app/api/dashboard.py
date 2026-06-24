"""Dashboard endpoints for sessions, metrics, pipeline, and activity."""

from __future__ import annotations

from fastapi import APIRouter, HTTPException, Query

from app.models import CreateSessionRequest, ProgressUpdateRequest
from app.services.session_manager import get_session_manager

router = APIRouter(prefix="/api/dashboard", tags=["dashboard"])


@router.post("/sessions", status_code=201)
def create_session(request: CreateSessionRequest):
    """Create a user session and run the five-agent preparation pipeline."""

    session = get_session_manager().create_session(
        user_id=request.user_id,
        name=request.name,
        email=request.email,
        current_role=request.current_role,
        target_role=request.target_role,
        resume_text=request.resume_text,
        experience_years=request.experience_years,
    )

    overview = get_session_manager().get_dashboard_data(session.session_id)
    return overview


@router.get("/sessions/{session_id}")
def get_session(session_id: str):
    """Return the complete dashboard view for one session."""

    overview = get_session_manager().get_dashboard_data(session_id)
    if overview is None:
        raise HTTPException(status_code=404, detail="Session not found")
    return overview


@router.get("/overview/{session_id}")
def get_dashboard_overview(session_id: str):
    """Alias used by dashboards that prefer an overview route."""

    return get_session(session_id)


@router.get("/metrics/{session_id}")
def get_metrics(session_id: str):
    """Return the numeric progress metrics for a session."""

    session = get_session_manager().get_session(session_id)
    if session is None:
        raise HTTPException(status_code=404, detail="Session not found")

    return get_session_manager().get_dashboard_data(session_id)["metrics"]


@router.get("/pipeline/{session_id}")
def get_pipeline_status(session_id: str):
    """Return the five-agent pipeline with status and agent outputs."""

    overview = get_session_manager().get_dashboard_data(session_id)
    if overview is None:
        raise HTTPException(status_code=404, detail="Session not found")

    return {
        "session_id": session_id,
        "pipeline": overview["pipeline"],
    }


@router.get("/activities/{session_id}")
def get_activities(session_id: str, limit: int = Query(10, ge=1, le=100)):
    """Return recent activity for one session, newest first."""

    session = get_session_manager().get_session(session_id)
    if session is None:
        raise HTTPException(status_code=404, detail="Session not found")

    activities = get_session_manager().get_activities(session_id, limit)
    return {
        "session_id": session_id,
        "activities": [
            activity.model_dump(mode="json")
            for activity in activities
        ],
        "total_count": len(activities),
    }


@router.put("/progress/{session_id}")
def update_progress(session_id: str, request: ProgressUpdateRequest):
    """Update progress metrics after practice, learning, or interviews."""

    session = get_session_manager().update_progress(
        session_id=session_id,
        overall_score=request.overall_score,
        questions_practiced=request.questions_practiced,
        interviews_taken=request.interviews_taken,
        current_streak_days=request.current_streak_days,
        learning_progress=request.learning_progress,
    )
    if session is None:
        raise HTTPException(status_code=404, detail="Session not found")

    return get_session_manager().get_dashboard_data(session_id)
