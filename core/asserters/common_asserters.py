from datetime import datetime
from typing import Any, Iterable, Literal, TypeVar, Union, Container
from urllib.parse import urlparse

import allure
import pytest_check as check
from pytest_check.check_functions import (
    _ComparableLessThanOrEqual,
    _ComparableGreaterThanOrEqual,
    _ComparableLessThan,
    _ComparableGreaterThan,
)
from requests import Response

T = TypeVar("T")
ComparisonSign = Literal["==", "<", "<=", ">", ">="]


@allure.step("Проверка, что {elements} in {container}")
def contains_all(container: Container[T], elements: Iterable[T]) -> None:
    missing = [item for item in elements if item not in container]
    check.is_false(
        x=missing,
        msg=f"Список {container} не содержит элементы {missing}",
    )


@allure.step("Проверка, что {elem} in {container}")
def is_in(elem: T, container: Container[T]) -> None:
    check.is_in(
        a=elem,
        b=container,
        msg=f"{container} не содержит элемент {elem}",
    )


@allure.step("[{prefix}] Сравнение actual ({actual}) и expected ({expected})")
def equal(
    actual: T,
    expected: T | None,
    prefix: str,
) -> None:
    check.equal(
        a=actual,
        b=expected,
        msg=f"[{prefix}] actual ({actual}) != expected ({expected})",
    )


@allure.step("Проверка, что {first} != {second}")
def not_equal(
    first: Any,
    second: Any,
    err_msg: str | None = None,
) -> None:
    default_message = f"{first} == {second}"
    check.not_equal(
        a=first,
        b=second,
        msg=err_msg or default_message,
    )


@allure.step("Проверка, что статус-код = {expected_code}")
def is_status_code(
    expected_code: int,
    response: Response,
    err_msg: str | None = None,
) -> None:
    actual_status_code = response.status_code
    default_err_msg = f"response.status_code {actual_status_code} != {expected_code}"
    check.equal(
        a=actual_status_code,
        b=expected_code,
        msg=err_msg or default_err_msg,
    )


@allure.step("Проверка, что {value} > 0")
def is_positive_num(value: Union[int, float]) -> None:
    check.greater(
        a=value,
        b=0,
        msg=f"value {value} <= 0",
    )


@allure.step("Проверка, что {url] начинается с http или https")
def is_valid_url(url: str) -> None:
    parsed_url = urlparse(url)
    schema_err = f"""
            Неверный URL '{url}':
                - Протокол должен быть 'http' или 'https'
            """
    check.is_in(
        a=parsed_url.scheme,
        b=("http", "https"),
        msg=schema_err,
    )


@allure.step("Проверка, что {actual} > {expected}")
def is_greater(
    actual: _ComparableGreaterThan,
    expected: object,
    prefix: str = "",
) -> None:
    check.greater(
        a=actual,
        b=expected,
        msg=f"[{prefix}] actual ({actual}) <= expected ({expected})",
    )


@allure.step("Проверка, что {actual} < {expected}")
def is_less(
    actual: _ComparableLessThan,
    expected: object,
    prefix: str = "",
) -> None:
    check.less(
        a=actual,
        b=expected,
        msg=f"[{prefix}] actual ({actual}) >= expected ({expected})",
    )


@allure.step("Проверка, что {actual} <= {expected}")
def is_less_equal(
    actual: _ComparableLessThanOrEqual,
    expected: object,
    prefix: str = "",
) -> None:
    check.less_equal(
        a=actual,
        b=expected,
        msg=f"[{prefix}] actual ({actual}) > expected ({expected})",
    )


@allure.step("Проверка, что {actual} >= {expected}")
def is_greater_equal(
    actual: _ComparableGreaterThanOrEqual,
    expected: object,
    prefix: str = "",
) -> None:
    check.greater_equal(
        a=actual,
        b=expected,
        msg=f"[{prefix}] actual ({actual}) < expected ({expected})",
    )


@allure.step("Проверка, что {actual} {comparison} {expected}")
def compare_dates(
    actual: datetime,
    expected: datetime,
    comparison: ComparisonSign = "==",
    prefix: str = "",
) -> None:
    match comparison:
        case "==":
            equal(actual=actual, expected=expected, prefix=prefix)
        case "<":
            is_less(actual=actual, expected=expected, prefix=prefix)
        case ">":
            is_greater(actual=actual, expected=expected, prefix=prefix)
        case "<=":
            is_less_equal(actual=actual, expected=expected, prefix=prefix)
        case ">=":
            is_greater_equal(actual=actual, expected=expected, prefix=prefix)
        case _:
            raise ValueError(f"Неизвестный оператор сравнения: {comparison}")


@allure.step("Проверка, что строка {value} не <blank>")
def is_not_blank_str(value: str, err_msg: str | None = None) -> None:
    check.is_false(
        x=value.isspace(),
        msg=err_msg or "str is blank",
    )


@allure.step("Проверка, что статус код ответа 201")
def is_status_code_201(response: Response) -> None:
    is_status_code(
        expected_code=201,
        response=response,
    )


@allure.step("Проверка, что статус код ответа = 200")
def is_status_code_200(response: Response) -> None:
    is_status_code(
        expected_code=200,
        response=response,
    )
