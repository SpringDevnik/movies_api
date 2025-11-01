from pydantic import BaseModel

from enums.auth.user_roles import UserRole


class Credentials(BaseModel):
    email: str
    password: str


class User(BaseModel):
    email: str
    password: str
    roles: list[UserRole]

    @property
    def creds(self) -> Credentials:
        """Возвращает кортеж (email, password)"""
        return Credentials(
            email=self.email,
            password=self.password,
        )
