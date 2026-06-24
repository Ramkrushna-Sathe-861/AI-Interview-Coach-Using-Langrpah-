"""
Data models for the Interview Coach system.

These Pydantic models define the structure of data flowing through the system,
ensuring type safety and clear documentation of what each API expects.
"""

from datetime import datetime
from enum import Enum
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


# ============================================================================
# Enumerations
# ============================================================================

class AgentStatus(str, Enum):
    """Status of an agent in the pipeline."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"


class InterviewDifficulty(str, Enum):
    """Difficulty level for mock interviews."""
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"


# ============================================================================
# User and Profile Models
# ============================================================================

class UserProfile(BaseModel):
    """User's basic profile information."""
    user_id: str
    name: str
    email: str
    current_role: str
    target_role: str
    experience_years: int = 0
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)


class UserResume(BaseModel):
    """Parsed resume information."""
    resume_id: str
    user_id: str
    raw_text: str
    parsed_skills: List[str] = Field(default_factory=list)
    experience: List[Dict[str, Any]] = Field(default_factory=list)
    education: List[Dict[str, Any]] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.now)


# ============================================================================
# Agent Models
# ============================================================================

class AgentTask(BaseModel):
    """Task assigned to an agent."""
    task_id: str
    agent_name: str
    status: AgentStatus = AgentStatus.PENDING
    input_data: Dict[str, Any]
    output_data: Optional[Dict[str, Any]] = None
    error_message: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None


class AgentPipelineStep(BaseModel):
    """Single step in the agent pipeline."""
    step_number: int
    agent_name: str
    agent_title: str
    description: str
    status: AgentStatus
    result: Optional[Dict[str, Any]] = None


class AgentPipeline(BaseModel):
    """Complete agent pipeline execution."""
    pipeline_id: str
    session_id: str
    user_id: str
    steps: List[AgentPipelineStep] = Field(default_factory=list)
    started_at: datetime = Field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None


# ============================================================================
# Skill Models
# ============================================================================

class Skill(BaseModel):
    """Skill with proficiency level."""
    name: str
    proficiency: float = Field(ge=0, le=100)  # 0-100%
    category: str = "general"


class SkillGapAnalysis(BaseModel):
    """Analysis of user's skills vs. target role requirements."""
    analysis_id: str
    user_id: str
    target_role: str
    strong_skills: List[Skill] = Field(default_factory=list)
    matched_skills: List[Skill] = Field(default_factory=list)
    missing_skills: List[Skill] = Field(default_factory=list)
    overall_match_score: float = Field(ge=0, le=100)
    created_at: datetime = Field(default_factory=datetime.now)


# ============================================================================
# Learning & Roadmap Models
# ============================================================================

class LearningModule(BaseModel):
    """Single learning module for a skill."""
    module_id: str
    skill_name: str
    title: str
    description: str
    estimated_hours: float
    difficulty: str


class LearningRoadmap(BaseModel):
    """Personalized learning roadmap for skill development."""
    roadmap_id: str
    user_id: str
    target_role: str
    modules: List[LearningModule] = Field(default_factory=list)
    total_estimated_hours: float = 0
    progress_percentage: float = Field(default=0, ge=0, le=100)
    created_at: datetime = Field(default_factory=datetime.now)


# ============================================================================
# Mock Interview Models
# ============================================================================

class InterviewQuestion(BaseModel):
    """Single interview question with context."""
    question_id: str
    question: str
    category: str
    difficulty: InterviewDifficulty
    hints: List[str] = Field(default_factory=list)


class InterviewResponse(BaseModel):
    """User's response to an interview question."""
    response_id: str
    question_id: str
    user_response: str
    timestamp: datetime = Field(default_factory=datetime.now)


class InterviewFeedback(BaseModel):
    """Feedback on a single response."""
    response_id: str
    score: float = Field(ge=0, le=10)
    strengths: List[str] = Field(default_factory=list)
    areas_to_improve: List[str] = Field(default_factory=list)
    suggestions: List[str] = Field(default_factory=list)


class MockInterview(BaseModel):
    """Complete mock interview session."""
    interview_id: str
    user_id: str
    session_id: str
    target_role: str
    difficulty: InterviewDifficulty
    questions: List[InterviewQuestion] = Field(default_factory=list)
    responses: List[InterviewResponse] = Field(default_factory=list)
    feedbacks: List[InterviewFeedback] = Field(default_factory=list)
    overall_score: float = Field(default=0, ge=0, le=10)
    duration_minutes: int = 0
    started_at: datetime = Field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None


# ============================================================================
# Session & Progress Models
# ============================================================================

class SessionProgress(BaseModel):
    """Overall progress in current session."""
    session_id: str
    user_id: str
    overall_score: float = Field(default=0, ge=0, le=100)
    questions_practiced: int = 0
    interviews_taken: int = 0
    current_streak_days: int = 0
    learning_progress: float = Field(default=0, ge=0, le=100)
    updated_at: datetime = Field(default_factory=datetime.now)


class UserSession(BaseModel):
    """User's current session with all data."""
    session_id: str
    user_id: str
    profile: UserProfile
    resume: Optional[UserResume] = None
    skill_gap_analysis: Optional[SkillGapAnalysis] = None
    learning_roadmap: Optional[LearningRoadmap] = None
    mock_interviews: List[MockInterview] = Field(default_factory=list)
    pipeline: Optional[AgentPipeline] = None
    progress: SessionProgress
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)


# ============================================================================
# Activity & Analytics Models
# ============================================================================

class ActivityLog(BaseModel):
    """Single user activity log entry."""
    activity_id: str
    user_id: str
    activity_type: str  # e.g., "interview_completed", "resume_analyzed"
    title: str
    description: str
    metadata: Dict[str, Any] = Field(default_factory=dict)
    timestamp: datetime = Field(default_factory=datetime.now)


class DashboardMetrics(BaseModel):
    """Dashboard overview metrics."""
    overall_progress: float = Field(ge=0, le=100)
    questions_practiced: int
    interviews_taken: int
    current_streak_days: int
    strong_skills: List[Skill] = Field(default_factory=list)
    weak_skills: List[Skill] = Field(default_factory=list)
    recent_activities: List[ActivityLog] = Field(default_factory=list)
    upcoming_interviews: List[MockInterview] = Field(default_factory=list)


# ============================================================================
# API Request/Response Models
# ============================================================================

class ChatRequest(BaseModel):
    """Chat endpoint request."""
    user_id: str
    session_id: str
    profile: str
    target_role: str
    history: str = "[]"


class ChatResponse(BaseModel):
    """Chat endpoint response."""
    session_id: str
    agent_response: str
    pipeline_status: List[AgentPipelineStep] = Field(default_factory=list)
    timestamp: datetime = Field(default_factory=datetime.now)


class CreateSessionRequest(BaseModel):
    """Request body for creating a dashboard session."""
    user_id: str
    name: str
    email: str
    current_role: str
    target_role: str
    resume_text: Optional[str] = None
    experience_years: int = Field(default=0, ge=0)


class ProgressUpdateRequest(BaseModel):
    """Request body for updating dashboard progress."""
    overall_score: Optional[float] = Field(default=None, ge=0, le=100)
    questions_practiced: Optional[int] = Field(default=None, ge=0)
    interviews_taken: Optional[int] = Field(default=None, ge=0)
    current_streak_days: Optional[int] = Field(default=None, ge=0)
    learning_progress: Optional[float] = Field(default=None, ge=0, le=100)


class DashboardResponse(BaseModel):
    """Dashboard data response."""
    session_id: str
    user: UserProfile
    metrics: DashboardMetrics
    pipeline: AgentPipeline
    timestamp: datetime = Field(default_factory=datetime.now)
