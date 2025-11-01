pytest_plugins = [
    "fixtures.movies_fixtures",
    "fixtures.auth_fixtures",
    "fixtures.common_fixtures",
    "core.plugins.allure_description_checker",
    # "core.plugins.xdist_logger", TODO: временно отключен из-за сырой функциональности
]
