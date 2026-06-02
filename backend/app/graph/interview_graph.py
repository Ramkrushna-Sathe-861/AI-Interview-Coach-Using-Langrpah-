from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from app.agents.resume_analyzer import ResumeAnalyzer
from app.agents.skill_gap_analyzer import SkillGapAnalyzer
from app.agents.roadmap_generator import RoadmapGenerator
from app.agents.question_generator import QuestionGenerator
from app.agents.mock_interviewer import MockInterviewer
from app.agents.feedback_generator import FeedbackGenerator
from app.services.llm_service import LLMService


class InterviewState(TypedDict, total=False):
    resume_text: str
    target_role: str
    resume_analysis: dict
    skill_gap_analysis: dict
    roadmap: dict
    questions: dict


class InterviewGraph:
    def __init__(self):
        llm = LLMService()
        self.resume_analyzer = ResumeAnalyzer(llm)
        self.skill_gap_analyzer = SkillGapAnalyzer(llm)
        self.roadmap_generator = RoadmapGenerator(llm)
        self.question_generator = QuestionGenerator(llm)
        self.mock_interviewer = MockInterviewer(llm)
        self.feedback_generator = FeedbackGenerator(llm)
        self.graph = self._build_graph()

    def _build_graph(self):
        graph = StateGraph(InterviewState)

        def analyze_resume(state: InterviewState) -> dict:
            return {"resume_analysis": self.resume_analyzer.analyze(state["resume_text"])}

        def analyze_skill_gap(state: InterviewState) -> dict:
            resume_analysis = state.get("resume_analysis", {})
            experience_summary = resume_analysis
            return {
                "skill_gap_analysis": self.skill_gap_analyzer.analyze(
                    resume_analysis,
                    experience_summary,
                    state["target_role"],
                )
            }

        def generate_roadmap(state: InterviewState) -> dict:
            return {
                "roadmap": self.roadmap_generator.generate(
                    state.get("resume_analysis", {}),
                    state["target_role"],
                )
            }

        def generate_questions(state: InterviewState) -> dict:
            return {
                "questions": self.question_generator.generate(
                    state["target_role"],
                    state.get("skill_gap_analysis", {}),
                )
            }

        graph.add_node("ResumeAnalyzer", analyze_resume)
        graph.add_node("SkillGapAnalyzer", analyze_skill_gap)
        graph.add_node("RoadmapGenerator", generate_roadmap)
        graph.add_node("QuestionGenerator", generate_questions)

        graph.add_edge(START, "ResumeAnalyzer")
        graph.add_edge("ResumeAnalyzer", "SkillGapAnalyzer")
        graph.add_edge("SkillGapAnalyzer", "RoadmapGenerator")
        graph.add_edge("RoadmapGenerator", "QuestionGenerator")
        graph.add_edge("QuestionGenerator", END)

        return graph.compile()

    def execute_resume_pipeline(self, resume_text: str, target_role: str) -> dict:
        state = self.graph.invoke({"resume_text": resume_text, "target_role": target_role})
        return {
            "resume_analysis": state.get("resume_analysis", {}),
            "skill_gap_analysis": state.get("skill_gap_analysis", {}),
            "roadmap": state.get("roadmap", {}),
            "questions": state.get("questions", {}),
        }
