import uuid
from tempfile import NamedTemporaryFile
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from fastapi.responses import JSONResponse
from app.services.resume_parser import ResumeParser
from app.graph.interview_graph import InterviewGraph
from app.graph.state import InterviewSession

router = APIRouter()
parser = ResumeParser()
graph = InterviewGraph()
sessions: dict[str, InterviewSession] = {}

@router.post("/upload-resume")
async def upload_resume(file: UploadFile = File(...)):
    if file.content_type not in ["application/pdf", "text/plain"]:
        raise HTTPException(status_code=400, detail="Only PDF and TXT resumes are supported.")

    with NamedTemporaryFile(delete=False, suffix=file.filename) as temp:
        contents = await file.read()
        temp.write(contents)
        temp.flush()
        resume_text = parser.extract_text(temp.name)

    session_id = str(uuid.uuid4())
    sessions[session_id] = InterviewSession(session_id=session_id, resume_text=resume_text)
    return {"session_id": session_id, "resume_text": resume_text[:1000]}

@router.post("/analyze")
def analyze_resume(session_id: str = Form(...), target_role: str = Form(...)):
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")

    session = sessions[session_id]
    session.target_role = target_role
    output = graph.execute_resume_pipeline(session.resume_text, target_role)
    session.resume_analysis = output["resume_analysis"]
    session.skill_gap_analysis = output["skill_gap_analysis"]
    session.roadmap = output["roadmap"]
    session.questions = output["questions"]
    session.profile = session.resume_analysis.get("analysis", "")

    return {
        "session_id": session_id,
        "resume_analysis": session.resume_analysis,
        "skill_gap_analysis": session.skill_gap_analysis,
        "roadmap": session.roadmap,
        "questions": session.questions,
    }

@router.post("/mock-interview")
def mock_interview(session_id: str = Form(...), answer: str = Form(""), question_history: str = Form("")):
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")

    session = sessions[session_id]
    history = question_history or "[]"
    interview_output = graph.mock_interviewer.ask(session.profile, session.target_role, history)
    session.history.append({"question": interview_output, "answer": answer})
    return {"session_id": session_id, "mock_interview": interview_output}

@router.post("/feedback")
def feedback(session_id: str = Form(...), responses: str = Form(...)):
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")

    session = sessions[session_id]
    context = {
        "resume_analysis": session.resume_analysis,
        "skill_gap_analysis": session.skill_gap_analysis,
        "roadmap": session.roadmap,
    }
    review_output = graph.feedback_generator.review(responses, str(context))
    session.feedback = review_output
    return {"session_id": session_id, "feedback": review_output}

@router.get("/session/{session_id}")
def get_session(session_id: str):
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    session = sessions[session_id]
    return JSONResponse(content={
        "session_id": session.session_id,
        "resume_text": session.resume_text,
        "target_role": session.target_role,
        "resume_analysis": session.resume_analysis,
        "skill_gap_analysis": session.skill_gap_analysis,
        "roadmap": session.roadmap,
        "questions": session.questions,
        "history": session.history,
        "feedback": session.feedback,
    })
