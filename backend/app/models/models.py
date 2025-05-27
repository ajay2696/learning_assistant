
from typing import List, Dict, Optional, Literal, Union
from pydantic import BaseModel, Field


class PreQuizReview(BaseModel):
    key_concepts_reminder: List[str]
    time_needed: str


class WarmUpQuestion(BaseModel):
    question_id: int
    type: Literal["multiple_choice"]
    difficulty: Literal["easy", "medium", "challenging"]
    question: str
    options: List[str]
    correct_answer: str
    explanation: str
    learning_objective: str
    time_estimate: str


class CoreConceptQuestion(BaseModel):
    question_id: int
    type: Literal["short_answer"]
    difficulty: Literal["easy", "medium", "challenging"]
    question: str
    sample_answer: str
    key_points: List[str]
    partial_credit_guide: str
    time_estimate: str


class ApplicationQuestion(BaseModel):
    question_id: int
    type: Literal["problem_solving"]
    difficulty: Literal["easy", "medium", "challenging"]
    question: str
    solution_steps: List[str]
    common_errors: List[str]
    hints: List[str]
    time_estimate: str


class ReflectionQuestion(BaseModel):
    question_id: int
    type: Literal["open_ended"]
    question: str
    guidance: str
    no_wrong_answer: bool
    time_estimate: str


class QuizContent(BaseModel):
    pre_quiz_review: PreQuizReview
    warm_up_questions: List[WarmUpQuestion]
    core_concept_questions: List[CoreConceptQuestion]
    application_questions: List[ApplicationQuestion]
    reflection_questions: List[ReflectionQuestion]


class QuizMetadata(BaseModel):
    total_questions: int
    estimated_time: str
    difficulty_distribution: Dict[str, int]
    learning_objectives_covered: List[str]
    question_type_distribution: Dict[str, int]


class ScoringGuide(BaseModel):
    total_possible_points: int
    excellent: str
    good: str
    needs_practice: str
    needs_help: str


class IfStruggling(BaseModel):
    immediate_support: str
    review_activities: str
    alternative_explanations: str


class IfExcelling(BaseModel):
    extension_activities: str
    enrichment_topics: str
    peer_teaching_opportunities: str


class GeneralFeedback(BaseModel):
    positive_reinforcement: str
    growth_mindset_messages: str
    next_steps: str


class AdaptiveSuggestions(BaseModel):
    if_struggling: IfStruggling
    if_excelling: IfExcelling
    general_feedback: GeneralFeedback


class QuizDay(BaseModel):
    day: int
    topic: str
    quiz_content: QuizContent
    quiz_metadata: QuizMetadata
    scoring_guide: ScoringGuide
    adaptive_suggestions: AdaptiveSuggestions



class VocabularyItem(BaseModel):
    term: str
    definition: str


class RealWorldExample(BaseModel):
    problem: str
    answer: str


class GuidedExample(BaseModel):
    example: str
    explanation: str


class Introduction(BaseModel):
    explanation: str
    key_concepts: List[str]
    prerequisites: List[str]
    why_it_matters: str


class MainContent(BaseModel):
    explanation: str
    visual_aids_description: str
    step_by_step_guide: List[str]
    real_world_examples: List[RealWorldExample]
    vocabulary: List[VocabularyItem]


class PracticeSection(BaseModel):
    guided_examples: List[GuidedExample]
    practice_problems: List[str]
    common_mistakes: List[str]
    success_tips: List[str]


class Summary(BaseModel):
    key_takeaways: List[str]
    connection_to_previous: str
    connection_to_next_day: str
    self_check_questions: List[str]


class DetailedContent(BaseModel):
    introduction: Introduction
    main_content: MainContent
    practice_section: PracticeSection
    summary: Summary


class EstimatedTimeBreakdown(BaseModel):
    introduction: str
    main_content: str
    practice: str
    summary: str


class DifferentiationOptions(BaseModel):
    struggling_students: str
    advanced_students: str
    different_learning_styles: str


class DayPlan(BaseModel):
    day: int
    topic: str
    detailed_content: DetailedContent
    estimated_time_breakdown: EstimatedTimeBreakdown
    differentiation_options: DifferentiationOptions



class StudyPlanItem(BaseModel):
    day: int = Field(description="Day number of the study plan.")
    topic: str = Field(description="The topic to be covered on this day.")
    duration: str = Field(description="Estimated time required for the topic.")


class StudyPlanOutput(BaseModel):
    study_plan: List[StudyPlanItem] = Field(description="List of study activities per day.")
    total_days: str = Field(description="Total number of days in the plan.")
    recommended_frequency: str = Field(description="How often the study plan should be followed.")
    additional_notes: str = Field(description="Extra tips or instructions for the study plan.")
