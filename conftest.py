import json
import os.path
from fixture.application import Application
import pytest
from fixture.db import DbFixture
from model.user import User

fixture = None
target = None


def load_config(file):
    global target
    if target is None:
        config_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), file)
        with open(config_file) as file:
            target = json.load(file)
    return target


@pytest.fixture
def app(request):
    global fixture
    web_config = load_config(request.config.getoption("--target"))
    if fixture is None or not fixture.is_valid():
        fixture = Application(browser=web_config["web"]["browser"], base_url=web_config["web"]["baseUrl"])
        fixture.session.ensure_login(User(username=web_config["adminweb"]["user"],
                                          password=web_config["adminweb"]["password"]))
    return fixture


@pytest.fixture(scope="session")
def db(request):
    web_config = load_config(request.config.getoption("--target"))["db"]
    dbfixture = DbFixture(host=web_config["host"], name=web_config["name"],
                          user=web_config["user"], password=web_config["password"])

    def fin():
        dbfixture.destroy()

    request.addfinalizer(fin)
    return dbfixture


@pytest.fixture
def check_ui(request):
    return request.config.getoption("--check_ui")


@pytest.fixture(scope="session", autouse=True)
def stop(request):
    def fin():
        fixture.session.ensure_logout()
        fixture.quit()

    request.addfinalizer(fin)
    return fixture


def pytest_addoption(parser):
    parser.addoption("--target", action="store", default="target.json")
