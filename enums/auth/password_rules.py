from dataclasses import dataclass
from enum import Enum


@dataclass(frozen=True)
class _PasswordRulesData:
    min_length: int
    max_length: int
    has_uppercase: bool
    has_lowercase: bool
    has_digit: bool
    has_special_char: bool


class PasswordRules(Enum):
    DEFAULT = _PasswordRulesData(
        min_length=8,
        max_length=20,
        has_uppercase=True,
        has_lowercase=True,
        has_digit=True,
        has_special_char=False,
    )
