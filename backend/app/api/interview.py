from fastapi import APIRouter, Form, HTTPException
from app.graph.interview_graph import ask_chat

router = APIRouter()


@router.post("/chat")
def chat(profile: str = Form(""), target_role: str = Form(""), history: str = Form("[]")):
    """Function-style chat endpoint that calls `ask_chat`.

    Uses simple function-level wiring for clarity and easy testing.
    """
    if not profile:
        raise HTTPException(status_code=400, detail="profile is required")

    output = ask_chat(profile, target_role, history)
    return {"mock_interview": output}
