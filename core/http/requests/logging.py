# mypy: ignore-missing-imports

from contextlib import suppress
from logging import Logger

import allure
import requests
from curlify2 import Curlify
from requests import PreparedRequest


def allure_log_request(prepared_request: PreparedRequest) -> None:
    allure.attach(
        body=Curlify(prepared_request).to_curl(),
        name="CURL",
        attachment_type=allure.attachment_type.TEXT,
    )


def local_log_request(logger: Logger, prepared_request: PreparedRequest) -> None:
    logger.info("=" * 80)
    logger.info("REQUEST CURL".center(80))
    logger.info(Curlify(prepared_request).to_curl())
    logger.info("=" * 80)


def local_log_response(logger: Logger, response: requests.Response) -> None:
    import json

    response_status = response.status_code
    response_data = response.text

    # Попытка форматировать JSON
    try:
        # Оставляем текст, если это не JSON
        with suppress(json.JSONDecodeError):
            response_data = json.dumps(json.loads(response.text), indent=4, ensure_ascii=False)

        # Логируем ответ
        logger.info(f"\n{'=' * 40} RESPONSE {'=' * 40}")
        logger.info(
            f"\tSTATUS_CODE: {response_status}\n" f"\tDATA: {response_data}",
        )
        logger.info(f"{'=' * 80}\n")
    except Exception as e:
        logger.error(f"\nLogging failed: {type(e)} - {e}")
