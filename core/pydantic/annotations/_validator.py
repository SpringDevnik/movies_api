def non_blank_str_validator(value: str) -> str:
    if value.isspace():
        raise ValueError("Значение является пустой строкой")
    return value
