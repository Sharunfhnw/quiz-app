import hashlib
from sqlmodel import select
from domain.models import User
class AuthService:
    """Business logic for authentification.
    Responsible for:
    - Passwort hashing with SHA256
    - Login validierung
    - New user registration
    - Passwort changes
    """
    def hash_password(self, password: str) -> str:
        """Hash the password using SHA256."""
        return hashlib.sha256(password.encode()).hexdigest()
    def check_password(
        self, password: str, stored_hash: str
    ) -> bool:
        """Compare the entered password with the stored hash."""
        return self.hash_password(password) == stored_hash
    def login(
        self, session, username: str, password: str
    ):
        """Search for users using username and password.
        Returns:
            User object if found, otherwise None
        """
        pw_hash = self.hash_password(password)
        return session.exec(
            select(User).where(
                User.username == username,
                User.password_hash == pw_hash
            )
        ).first()
    def register(
        self,
        session,
        username: str,
        email: str,
        password: str,
        role: str
    ) -> User:
        """Create a new user and save it in the database."""
        user = User(
            username=username,
            email=email,
            password_hash=self.hash_password(password),
            role=role
        )
        session.add(user)
        session.commit()
        return user
    def change_password(
        self,
        session,
        user: User,
        old_password: str,
        new_password: str
    ) -> bool:
        """Change password after validating the old password.
        Returns:
            True if successful, False if old password is incorrect
        """
        if not self.check_password(old_password, user.password_hash):
            return False
        user.password_hash = self.hash_password(new_password)
        session.add(user)
        session.commit()
        return True