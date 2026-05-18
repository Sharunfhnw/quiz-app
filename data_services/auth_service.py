import hashlib
from sqlmodel import select
from domain.models import User
class AuthService:
    """Businesslogik fuer Authentifizierung.
    Verantwortlich fuer:
    - Passwort-Hashing mit SHA256
    - Login-Validierung
    - Registrierung neuer User
    - Passwort-Aenderung
    """
    def hash_password(self, password: str) -> str:
        """Passwort mit SHA256 hashen."""
        return hashlib.sha256(password.encode()).hexdigest()
    def check_password(
        self, password: str, stored_hash: str
    ) -> bool:
        """Eingegebenes Passwort mit gespeichertem Hash vergleichen."""
        return self.hash_password(password) == stored_hash
    def login(
        self, session, username: str, password: str
    ):
        """User anhand Username und Passwort suchen.
        Returns:
            User-Objekt wenn gefunden, sonst None
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
        """Neuen User erstellen und in DB speichern."""
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
        """Passwort aendern nach Validierung des alten Passworts.
        Returns:
            True wenn erfolgreich, False wenn altes Passwort falsch
        """
        if not self.check_password(old_password, user.password_hash):
            return False
        user.password_hash = self.hash_password(new_password)
        session.add(user)
        session.commit()
        return True