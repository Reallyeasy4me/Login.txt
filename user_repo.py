from sqlalchemy.orm import Session
from passlib.context import CryptContext
from db import DBUser          # модель пользователя в БД
from user import UserRole      # Enum ролей (admin/user)


pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")


class UserRepo:
    def __init__(self, db: Session):
        self.db = db

    def get_by_email(self, email: str):
        """Найти пользователя по email."""
        return self.db.query(DBUser).filter(DBUser.email == email).first()

    def create_user(self, email: str, password: str, role: UserRole):
        """Создать нового пользователя."""

        # Для pbkdf2_sha256 нет ограничения 72 байта, можно не резать пароль
        hashed_password = pwd_context.hash(password)

        user = DBUser(email=email, hashed_password=hashed_password, role=role)
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Проверить пароль."""
        return pwd_context.verify(plain_password, hashed_password)