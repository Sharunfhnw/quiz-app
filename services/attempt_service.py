from sqlmodel import select
from domain.models import QuizAttempt, StudentAnswer
class AttemptService:
    """Business logic for quiz attempts and score calculation.
    Responsibilities:
    - Calculate the score as a percentage
    - Retrieve attempts (by student, by quiz)
    - Calculate the average
    """
    def calculate_percentage(
        self, score: float, max_score: float
    ) -> float:
        """Convert the score to a percentage.
        Example: score=4, max_score=5 → 80.0
        """
        if max_score == 0:
            return 0.0
        return round(score / max_score * 100, 1)
    def get_attempts_by_student(
        self, session, student_id: int
    ) -> list:
        """Return all of a student's attempts."""
        return session.exec(
            select(QuizAttempt).where(
                QuizAttempt.student_id == student_id
            )
        ).all()
    def get_attempts_by_quiz(
        self, session, quiz_id: int
    ) -> list:
        """Return all attempts for a quiz."""
        return session.exec(
            select(QuizAttempt).where(
                QuizAttempt.quiz_id == quiz_id
            )
        ).all()
    def get_average(self, attempts: list) -> float:
        """Calculate the average score for a list of experiments."""
        if not attempts:
            return 0.0
        return round(
            sum(
                a.score / a.max_score * 100
                for a in attempts
            ) / len(attempts),
            1
        )
    def get_best(self, attempts: list) -> float:
        """Best result from a list of experiments."""
        if not attempts:
            return 0.0
        return max(
            a.score / a.max_score * 100
            for a in attempts
        )