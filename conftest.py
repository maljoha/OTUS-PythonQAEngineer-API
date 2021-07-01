import pytest

DOG_URL = "https://dog.ceo/api/"
BREWERIES_URL = "https://api.openbrewerydb.org/breweries/"
JSON_PH_URL = "https://jsonplaceholder.typicode.com/"


def pytest_addoption(parser):
    parser.addoption(
        "--url",
        action="store",
        default="https://ya.ru",
        help="This is request url"
    )
    parser.addoption(
        "--status_code",
        action="store",
        default=200,
        help="This is status code"
    )


@pytest.fixture(scope="session")
def url(request):
    return request.config.getoption("--url")


@pytest.fixture(scope="session")
def status_code(request):
    return request.config.getoption("--status_code")
