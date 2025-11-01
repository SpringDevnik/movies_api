from datetime import datetime
from functools import partial

from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel

from core.pydantic.annotations.type import NonBlankStr
from core.utils.fake import faker, generate_password
from enums.auth.password_rules import PasswordRules
from enums.auth.user_roles import UserRole


class UserData(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
    )

    id: NonBlankStr = Field(default_factory=faker.uuid4)
    email: NonBlankStr = Field(default_factory=faker.email)
    full_name: NonBlankStr = Field(default_factory=faker.name)
    password: NonBlankStr = Field(
        default_factory=partial(
            generate_password,
            min_length=PasswordRules.DEFAULT.value.min_length,
            max_length=PasswordRules.DEFAULT.value.max_length,
            has_special_char=PasswordRules.DEFAULT.value.has_special_char,
            has_digit=PasswordRules.DEFAULT.value.has_digit,
            has_uppercase=PasswordRules.DEFAULT.value.has_uppercase,
            has_lowercase=PasswordRules.DEFAULT.value.has_lowercase,
        ),
    )
    roles: list[UserRole] = Field(
        default_factory=lambda: [UserRole.USER],
    )
    verified: bool = Field(default_factory=faker.boolean)
    created_at: datetime = datetime.now()
    banned: bool = Field(default_factory=faker.boolean)
