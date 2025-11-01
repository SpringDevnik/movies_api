import logging
import os
import threading
import traceback
from datetime import datetime
from logging import Logger
from pathlib import Path
from typing import Any, Generator, Iterator, cast

import pytest
from _pytest.nodes import Item
from _pytest.stash import StashKey

# TODO следует насыщать только в pytest_runtest_logreport, ибо будет вызываемым мастер-логгером в мастер-процессе
_master_failed_test_logs = {}
# TODO добавить механизм синхронизации даты между воркерами посредством filelock
_session_datetime = datetime.now().strftime("%Y%m%d_%H%M%S")
_thread_locals = threading.local()
worker_id_key = StashKey[str]()
test_env_key = StashKey[str]()
log_base_dir_key = StashKey[Path]()
test_logger_key = StashKey[Logger]()
log_file_path_key = StashKey[Path]()


# TODO добавить механизм рекурсивного удаления старых логов
@pytest.hookimpl
def pytest_configure(config: pytest.Config) -> None:
    """
    Добавляем в объект pytest.Config следующие атрибуты:
    - worker_id - значение переменной окружения PYTEST_XDIST_WORKER ("master" по умолчанию)
    - test_env - значение переменной окружения TEST_ENV ("local" по умолчанию)
    - log_base_dir - директория, в которой хранятся логи тестов
    """

    worker_id = os.getenv("PYTEST_XDIST_WORKER", "master")
    test_env = os.getenv("TEST_ENV", "local")
    log_base_dir = Path("artifacts") / "logs" / test_env / _session_datetime
    log_base_dir.mkdir(parents=True, exist_ok=True)

    config.stash.setdefault(worker_id_key, worker_id)
    config.stash.setdefault(test_env_key, test_env)
    config.stash.setdefault(test_env_key, test_env)
    config.stash.setdefault(log_base_dir_key, log_base_dir)


# TODO подумать по поводу логирования тестов с маркировками skip и т.п.и
# TODO подумать о переносе маркировки фаз в pytest_runtest_makereport
@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_setup(item: pytest.Item) -> Iterator:
    _setup_test_logger(item)

    if hasattr(item, "test_logger"):
        set_test_logger(item.test_logger)

    yield


@pytest.hookimpl(hookwrapper=True, trylast=True)
def pytest_runtest_makereport(item: pytest.Item) -> Generator[None, pytest.TestReport, None]:
    outcome = yield
    report: pytest.TestReport = outcome.get_result()

    if hasattr(item, "log_file_path"):
        log_path = item.log_file_path

        if report.when == "call":
            item.add_report_section(
                when="call",
                key="log_file",
                content=f"Log: {log_path.absolute()}",  # TODO разобраться, почему не работает
            )


@pytest.hookimpl(trylast=True)
def pytest_runtest_teardown(item: Item) -> None:
    """
    Cleanup после теста - закрываем handlers.
    trylast=True - выполняется после всех остальных teardown.
    """
    if hasattr(item, "test_logger"):
        logger = item.test_logger
        logger.info("=" * 80)
        logger.info(f"Test finished: {datetime.now().isoformat()}")
        logger.info("=" * 80)

        for handler in logger.handlers[:]:
            handler.close()
            logger.removeHandler(handler)

    clear_test_logger()


@pytest.hookimpl(hookwrapper=True)
def pytest_exception_interact(
    node: pytest.Item | pytest.Collector,
    call: pytest.CallInfo[Any],
) -> Iterator:
    yield

    if not hasattr(node, "test_logger"):
        return

    logger = node.stash[test_logger_key]
    log_path = node.stash[log_file_path_key]
    excinfo: pytest.ExceptionInfo[BaseException] = cast(pytest.ExceptionInfo[BaseException], call.excinfo)

    try:
        if excinfo:
            logger.error("=" * 80)
            logger.error("🚨 TEST FAILED WITH EXCEPTION")
            logger.error("=" * 80)

            exception_type = excinfo.type
            exception_value = excinfo.value
            exception_traceback = excinfo.tb

            logger.error(f"Exception Type: {exception_type.__name__}")
            logger.error(f"Exception Module: {exception_type.__module__}")
            logger.error("=" * 80)

            logger.error(f"Exception Message: {str(exception_value)}")

            if hasattr(exception_value, "__dict__") and exception_value.__dict__:
                logger.error(f"Exception Attributes: {exception_value.__dict__}")

            logger.error("=" * 80)
            logger.error("FORMATTED TRACEBACK:")
            logger.error("=" * 80)

            tb_formatted = "".join(
                traceback.format_exception(
                    exception_type,
                    exception_value,
                    exception_traceback,
                ),
            )
            for line in tb_formatted.split("\n"):
                if line:
                    logger.error(line)

            logger.error("=" * 80)
            # TODO ОПАСНО! Данные пишутся в глобальную переменнную воркера. Не доступно в мастер процессе
            _master_failed_test_logs[node.nodeid] = str(log_path.absolute())
    except Exception as log_error:
        logger.error(f"⚠️ Failed to log exception details: {log_error}")
        logger.error(f"Original exception: {excinfo.typename}: {excinfo.value}")

    finally:
        for handler in logger.handlers:
            try:
                handler.flush()
            except Exception as e:
                print(f"⚠️ Warning: Failed to flush handler: {e}")


@pytest.hookimpl
def pytest_terminal_summary(terminalreporter: pytest.TerminalReporter) -> None:
    if not _master_failed_test_logs:
        return

    terminalreporter.ensure_newline()
    terminalreporter.section("🔴 Failed Test Logs", sep="=", red=True, bold=True)
    terminalreporter.write_line("")

    for nodeid, log_path in _master_failed_test_logs.items():
        short_name = nodeid.split("::")[-1]

        terminalreporter.write_line(f"❌ {short_name}", red=True, bold=True)
        terminalreporter.write_line(f'  📁 "{log_path}"')
        terminalreporter.write_line(f"  💻 Open with: cat {log_path}", cyan=True)
        terminalreporter.write_line("")


def _setup_test_logger(item: Item) -> None:
    """
    Создаёт изолированный логгер для каждого теста.

    Критичные моменты:
    - Уникальное имя логгера (предотвращает коллизии)
    - Отдельный FileHandler на каждый тест
    - Propagate=False (изоляция от root logger)
    """
    config = item.config
    worker_id: str = config.stash[worker_id_key]
    test_env: str = config.stash[test_env_key]
    test_execution_count = getattr(item, "execution_count", 0)

    test_name = item.nodeid.replace("::", "-").replace("/", "_").replace("[", "_").replace("]", "")
    log_file_name = f"{worker_id}_{test_execution_count}_{test_name}.log"
    log_file_path = config.stash[log_base_dir_key] / log_file_name

    logger_name = f"test.{worker_id}.{item.nodeid}"
    logger = logging.getLogger(logger_name)

    logger.handlers.clear()
    logger.setLevel(logging.DEBUG)
    logger.propagate = False

    file_handler = logging.FileHandler(
        filename=log_file_path,
        mode="w",
        encoding="utf-8",
        delay=False,
    )
    file_handler.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)

    logger.info("=" * 80)
    logger.info(f"Test: {item.nodeid}")
    logger.info(f"Worker: {worker_id}")
    logger.info(f"Environment: {test_env}")
    logger.info(f"Test execution count: {test_execution_count}")
    logger.info(f"Started: {datetime.now().isoformat()}")
    logger.info("=" * 80)

    item.stash.setdefault(test_logger_key, logger)
    item.stash.setdefault(log_file_path_key, log_file_path)


def get_item_logger() -> logging.Logger | None:
    """
    Получает логгер текущего теста.

    Использование в ЛЮБОЙ функции/враппере:
        from utils.logger import get_test_logger

        def my_wrapper():
            logger = get_test_logger()
            if logger:
                logger.info("Log from wrapper")
    """
    return getattr(_thread_locals, "logger", None)


def set_test_logger(logger: logging.Logger) -> None:
    """Устанавливает логгер для текущего потока"""
    _thread_locals.logger = logger


def clear_test_logger() -> None:
    """Очищает логгер текущего потока"""
    if hasattr(_thread_locals, "logger"):
        delattr(_thread_locals, "logger")
