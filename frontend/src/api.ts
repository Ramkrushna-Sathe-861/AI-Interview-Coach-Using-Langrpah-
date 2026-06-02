const API_BASE = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000/api/interview";

export async function uploadResume(file: File) {
  const form = new FormData();
  form.append("file", file);

  const response = await fetch(`${API_BASE}/upload-resume`, {
    method: "POST",
    body: form,
  });

  if (!response.ok) {
    throw new Error("Failed to upload resume");
  }

  return response.json();
}

export async function analyzeResume(sessionId: string, targetRole: string) {
  const form = new FormData();
  form.append("session_id", sessionId);
  form.append("target_role", targetRole);

  const response = await fetch(`${API_BASE}/analyze`, {
    method: "POST",
    body: form,
  });

  if (!response.ok) {
    throw new Error("Failed to analyze resume");
  }

  return response.json();
}

export async function mockInterview(sessionId: string, answer: string, questionHistory: string) {
  const form = new FormData();
  form.append("session_id", sessionId);
  form.append("answer", answer);
  form.append("question_history", questionHistory || "[]");

  const response = await fetch(`${API_BASE}/mock-interview`, {
    method: "POST",
    body: form,
  });

  if (!response.ok) {
    throw new Error("Failed to get mock interview question");
  }

  return response.json();
}

export async function sendFeedback(sessionId: string, responses: string) {
  const form = new FormData();
  form.append("session_id", sessionId);
  form.append("responses", responses);

  const response = await fetch(`${API_BASE}/feedback`, {
    method: "POST",
    body: form,
  });

  if (!response.ok) {
    throw new Error("Failed to send feedback request");
  }

  return response.json();
}

export async function getSession(sessionId: string) {
  const response = await fetch(`${API_BASE}/session/${sessionId}`);
  if (!response.ok) {
    throw new Error("Failed to fetch session");
  }

  return response.json();
}
