"""LearnLoop domain models.
Defines all database tables using SQLModel.
Each class represents one table in the SQLite database.
"""
from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
class User(SQLModel, table=True):
    """Represents a user in the system.
    Attributes:
        id: Auto-generated primary key.
        username: Unique login name.
        email: Email address of the user.
        password_hash: SHA256 hashed password (never stored plain).
        role: Either 'teacher' or 'student'.
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str
    email: str
    password_hash: str
    role: str  # 'teacher' or 'student'
class Quiz(SQLModel, table=True):
    """Represents a quiz created by a teacher.
    Attributes:
        id: Auto-generated primary key.
        title: Display name of the quiz.
        description: Short description shown to students.
        is_published: If True, students can see and attempt the quiz.
        teacher_id: Foreign key to the User who created the quiz.
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    description: str
    is_published: bool = False  # Draft by default
    teacher_id: int = Field(foreign_key='user.id')
class Question(SQLModel, table=True):
    """Represents a single question inside a quiz.
    Attributes:
        id: Auto-generated primary key.
        text: The question text shown to the student.
        quiz_id: Foreign key to the Quiz this question belongs to.
        question_type: Determines how the question is displayed.
            'single'    = Single Choice (radio button, one correct answer)
            'multiple'  = Multiple Choice (checkboxes, partial scoring)
            'truefalse' = True/False (two buttons, Wahr/Falsch)
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    text: str
    quiz_id: int = Field(foreign_key='quiz.id')
    question_type: str = Field(default='single')
class AnswerOption(SQLModel, table=True):
    """Represents one answer option for a question.
    Attributes:
        id: Auto-generated primary key.
        text: The answer text shown to the student.
        is_correct: True if this is a correct answer.
        question_id: Foreign key to the Question this belongs to.
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    text: str
    is_correct: bool
    question_id: int = Field(foreign_key='question.id')
class QuizAttempt(SQLModel, table=True):
    """Represents one attempt by a student to complete a quiz.
    Attributes:
        id: Auto-generated primary key.
        student_id: Foreign key to the User (student) who attempted.
        quiz_id: Foreign key to the Quiz that was attempted.
        score: Achieved score (float to support partial scoring).
        max_score: Maximum possible score for the quiz.
        completed_at: Timestamp when the attempt was submitted.
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    student_id: int = Field(foreign_key='user.id')
    quiz_id: int = Field(foreign_key='quiz.id')
    score: float = Field(default=0.0)      # Float for partial scoring
    max_score: float = Field(default=0.0)  # Float for partial scoring
    completed_at: datetime = Field(default_factory=datetime.now)
class StudentAnswer(SQLModel, table=True):
    """Represents the answer a student gave for one question.
    Attributes:
        id: Auto-generated primary key.
        attempt_id: Foreign key to the QuizAttempt.
        question_id: Foreign key to the Question that was answered.
        selected_answer_option_id: The chosen AnswerOption (optional
            for True/False where no option ID is stored on wrong answer).
        is_correct: True if the answer was correct.
        partial_score: Points earned (0.0-1.0, supports partial credit
            for Multiple Choice questions).
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    attempt_id: int = Field(foreign_key='quizattempt.id')
    question_id: int = Field(foreign_key='question.id')
    # Optional: not set for wrong True/False answers
    selected_answer_option_id: Optional[int] = Field(
        default=None, foreign_key='answeroption.id'
    )
    is_correct: bool
    # Partial credit for Multiple Choice (0.0 to 1.0)
    partial_score: float = Field(default=0.0)