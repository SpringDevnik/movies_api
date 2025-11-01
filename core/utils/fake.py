from faker import Faker

faker = Faker(locale="RU_ru")


def generate_password(
    min_length: int = 8,
    max_length: int = 20,
    has_special_char: bool = True,
    has_digit: bool = True,
    has_uppercase: bool = True,
    has_lowercase: bool = True,
) -> str:
    password_length = faker.random_int(min=min_length, max=max_length)
    return faker.password(
        length=password_length,
        special_chars=has_special_char,
        digits=has_digit,
        upper_case=has_uppercase,
        lower_case=has_lowercase,
    )
