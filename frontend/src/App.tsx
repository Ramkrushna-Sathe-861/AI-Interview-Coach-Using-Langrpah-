import { useMemo, useState } from "react";
import { analyzeResume, getSession, mockInterview, sendFeedback, uploadResume } from "./api";

const initialQuestions = "[]";

function App() {
  const [sessionId, setSessionId] = useState("");
  const [resumeFile, setResumeFile] = useState<File | null>(null);
  const [targetRole, setTargetRole] = useState("Software Engineer");
  const [status, setStatus] = useState("Ready to start");
  const [resumeAnalysis, setResumeAnalysis] = useState<string>("");
  const [skillGapAnalysis, setSkillGapAnalysis] = useState<string>("");
  const [roadmap, setRoadmap] = useState<string>("");
  const [questions, setQuestions] = useState<string>("");
  const [interviewQuestion, setInterviewQuestion] = useState<string>("");
  const [answer, setAnswer] = useState<string>("");
  const [questionHistory, setQuestionHistory] = useState<string>(initialQuestions);
  const [feedbackResponse, setFeedbackResponse] = useState<string>("");
  const [responses, setResponses] = useState<string>("");
  const [error, setError] = useState<string>("");

  const canAnalyze = !!sessionId && !!targetRole;
  const canMock = !!sessionId;

  const history = useMemo(() => {
    try {
      return JSON.parse(questionHistory) as Array<{ question: string; answer: string }>;
    } catch {
      return [];
    }
  }, [questionHistory]);

  const resetError = () => setError("");

  const handleUpload = async () => {
    if (!resumeFile) {
      setError("Please select a resume file.");
      return;
    }

    resetError();
    setStatus("Uploading resume...");

    try {
      const body = await uploadResume(resumeFile);
      setSessionId(body.session_id);
      setStatus("Resume uploaded. Ready to analyze.");
    } catch (err) {
      setError((err as Error).message);
      setStatus("Upload failed.");
    }
  };

  const handleAnalyze = async () => {
    if (!sessionId) {
      setError("Create a session first.");
      return;
    }

    resetError();
    setStatus("Analyzing resume...");

    try {
      const body = await analyzeResume(sessionId, targetRole);
      setResumeAnalysis(body.resume_analysis?.analysis || "No resume analysis returned.");
      setSkillGapAnalysis(body.skill_gap_analysis?.skill_gap_analysis || "No skill gap analysis returned.");
      setRoadmap(body.roadmap?.roadmap || "No roadmap returned.");
      setQuestions(body.questions?.questions || "No questions returned.");
      setStatus("Analysis complete.");
    } catch (err) {
      setError((err as Error).message);
      setStatus("Analysis failed.");
    }
  };

  const handleMockInterview = async () => {
    if (!sessionId) {
      setError("Create a session first.");
      return;
    }

    resetError();
    setStatus("Running mock interview...");

    try {
      const body = await mockInterview(sessionId, answer, questionHistory);
      const nextQuestion = body.mock_interview || body.question || "No question returned.";
      setInterviewQuestion(nextQuestion);
      setStatus("Mock interview question received.");

      const nextHistory = [...history, { question: nextQuestion, answer }];
      setQuestionHistory(JSON.stringify(nextHistory));
      setAnswer("");
    } catch (err) {
      setError((err as Error).message);
      setStatus("Mock interview failed.");
    }
  };

  const handleFeedback = async () => {
    if (!sessionId) {
      setError("Create a session first.");
      return;
    }

    resetError();
    setStatus("Sending feedback...");

    try {
      const body = await sendFeedback(sessionId, responses);
      setFeedbackResponse(body.feedback || JSON.stringify(body, null, 2));
      setStatus("Feedback received.");
    } catch (err) {
      setError((err as Error).message);
      setStatus("Feedback failed.");
    }
  };

  const loadSession = async () => {
    if (!sessionId) {
      setError("Enter a session id before loading.");
      return;
    }

    resetError();
    setStatus("Loading session...");

    try {
      const body = await getSession(sessionId);
      setResumeAnalysis(JSON.stringify(body.resume_analysis || {}, null, 2));
      setSkillGapAnalysis(JSON.stringify(body.skill_gap_analysis || {}, null, 2));
      setRoadmap(JSON.stringify(body.roadmap || {}, null, 2));
      setQuestions(JSON.stringify(body.questions || {}, null, 2));
      setStatus("Session loaded.");
    } catch (err) {
      setError((err as Error).message);
      setStatus("Session load failed.");
    }
  };

  return (
    <div className="app-shell">
      <header className="hero">
        <div>
          <p className="eyebrow">InterviewCoach</p>
          <h1>React frontend for your AI Interview backend</h1>
          <p className="subtitle">
            Upload a resume, analyze it, run mock interviews, and gather feedback without leaving the browser.
          </p>
        </div>
        <div className="status-pill">{status}</div>
      </header>

      <main>
        <section className="card grid-2">
          <div>
            <h2>Resume session</h2>
            <label className="label">Resume file</label>
            <input
              type="file"
              accept=".pdf,.txt"
              onChange={(event) => setResumeFile(event.target.files?.[0] ?? null)}
            />
            <label className="label">Target role</label>
            <input
              type="text"
              value={targetRole}
              onChange={(event) => setTargetRole(event.target.value)}
            />
            <button className="button primary" onClick={handleUpload}>Upload Resume</button>
            <button className="button" disabled={!sessionId} onClick={handleAnalyze}>Analyze Resume</button>
            <div className="field-row">
              <span className="badge">Session:</span>
              <code>{sessionId || "No session yet"}</code>
            </div>
          </div>

          <div>
            <h2>Import existing session</h2>
            <label className="label">Session ID</label>
            <input
              type="text"
              value={sessionId}
              onChange={(event) => setSessionId(event.target.value)}
            />
            <button className="button" onClick={loadSession}>Load session</button>
            <p className="help-text">
              Paste a session id to reload analysis results and continue the interview flow.
            </p>
          </div>
        </section>

        <section className="card grid-3">
          <div>
            <h3>Resume analysis</h3>
            <pre>{resumeAnalysis || "No analysis yet."}</pre>
          </div>
          <div>
            <h3>Skill gap</h3>
            <pre>{skillGapAnalysis || "No skill gap yet."}</pre>
          </div>
          <div>
            <h3>Roadmap</h3>
            <pre>{roadmap || "No roadmap yet."}</pre>
          </div>
        </section>

        <section className="card">
          <h2>Mock interview</h2>
          <div className="field-row">
            <div className="mock-panel">
              <h4>Question</h4>
              <p>{interviewQuestion || "Press the button to generate a mock question."}</p>
            </div>
            <div className="mock-panel">
              <h4>Your answer</h4>
              <textarea
                value={answer}
                onChange={(event) => setAnswer(event.target.value)}
                placeholder="Type your answer here"
              />
            </div>
          </div>
          <button className="button primary" disabled={!canMock} onClick={handleMockInterview}>
            Generate mock interview question
          </button>
        </section>

        <section className="card">
          <h2>Question history</h2>
          <textarea
            rows={8}
            value={questionHistory}
            onChange={(event) => setQuestionHistory(event.target.value)}
          />
        </section>

        <section className="card grid-2">
          <div>
            <h2>Feedback</h2>
            <textarea
              rows={6}
              placeholder="Paste your interview responses or write what you want feedback on"
              value={responses}
              onChange={(event) => setResponses(event.target.value)}
            />
            <button className="button" onClick={handleFeedback}>Request feedback</button>
          </div>
          <div>
            <h3>Feedback result</h3>
            <pre>{feedbackResponse || "No feedback yet."}</pre>
          </div>
        </section>

        {error ? (
          <div className="banner error">
            <strong>Error:</strong> {error}
          </div>
        ) : null}
      </main>
    </div>
  );
}

export default App;
