export type SessionResponse = {
  session_id: string;
  resume_text?: string;
  resume_analysis?: Record<string, any>;
  skill_gap_analysis?: Record<string, any>;
  roadmap?: Record<string, any>;
  questions?: Record<string, any>;
  history?: Array<{ question: string; answer: string }>;
  feedback?: Record<string, any>;
};

export type InterviewState = {
  sessionId: string;
  resumeText: string;
  targetRole: string;
  resumeAnalysis: string;
  skillGapAnalysis: string;
  roadmap: string;
  questions: string;
  interviewQuestion: string;
  answer: string;
  questionHistory: string;
  feedbackResponse: string;
  status: string;
  error: string;
};
