from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.interview import router as interview_router

app = FastAPI(
    title="InterviewPilot-AI Backend",
    description="Agentic AI backend for resume analysis, skill-gap planning, mock interviews, and feedback.",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(interview_router, prefix="/api/interview")

@app.get("/")
def root():
    return {"service": "InterviewPilot-AI Backend", "status": "ready"}

