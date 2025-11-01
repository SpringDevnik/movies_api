# from textwrap import dedent
#
# import pytest
# from allure_pytest.utils import ALLURE_DESCRIPTION_MARK
#
#
# @pytest.hookimpl
# def pytest_collection_modifyitems(items: list[pytest.Item]):
#     missing_annotation: list[str] = []
#
#     for item in items:
#         description_mark = next((mark for mark in item.own_markers if mark.name == ALLURE_DESCRIPTION_MARK), None)
#         if description_mark:
#             description = description_mark.args[0]
#             item.user_properties.append(("description", description))
#         else:
#             missing_annotation.append(item.nodeid)
#
#     if missing_annotation:
#         tests = "\n".join(f"\t{idx}. {elem}" for idx, elem in enumerate(missing_annotation, 1))
#         err_msg = dedent(
#             f"""\
# The following tests are missing mark '@allure.description':
#
# {tests}
#             """,
#         )
#         pytest.exit(err_msg)
#
#
# @pytest.hookimpl(hookwrapper=True)
# def pytest_runtest_logreport(report: pytest.TestReport):
#     yield
#     if report.when == "teardown" or report.outcome in ("skipped", "failed"):
#         description = dict(report.user_properties).get("description")
#         if description:
#             print("\n" + description)
#         print("-" * 40)
#
