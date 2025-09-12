from enum import Enum


class PasswordRule(Enum):
    MIN_LENGTH = 8
    MAX_LENGTH = 20
    HAS_UPPERCASE = True
    HAS_LOWERCASE = True
    HAS_DIGIT = True
    HAS_SPECIAL_CHAR = False