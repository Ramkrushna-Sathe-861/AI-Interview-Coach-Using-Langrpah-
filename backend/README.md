# InterviewPilot-AI Backend

A production-style Python backend for InterviewPilot-AI using FastAPI, LangGraph, and OpenAI.

## Features

- Resume upload and parsing
- Resume skill extraction
- Skill-gap analysis for a target role
- Learning roadmap generation
- Interview question generation
- Mock interview orchestration
- Feedback generation and scoring

## Quick start

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Create a `.env` file with your Groq or OpenAI credentials:
   ```text
   # Groq provider example
   GROQ_API_KEY=your_groq_api_key_here
   GROQ_MODEL=meta-llama/llama-4-scout-17b-16e-instruct
   LLM_PROVIDER=groq
   LANGGRAPH_API_KEY=your_langgraph_api_key_here

   # Or OpenAI provider example
   # OPENAI_API_KEY=your_openai_api_key_here
   # OPENAI_MODEL=gpt-4.1-mini
   # LLM_PROVIDER=openai
   ```

3. Run the app from the `backend` folder:
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

4. API endpoints:
   - `POST /api/interview/upload-resume`
   - `POST /api/interview/analyze`
   - `POST /api/interview/mock-interview`
   - `POST /api/interview/feedback`
   - `GET /api/interview/session/{session_id}`
