from dataclasses import dataclass

from api.api_manager import ApiManager
from models.api.user import User


@dataclass(frozen=True)
class UserContext:
    user: User
    api_manager: ApiManager
