import json
import os.path
from fixture.application import Application
import pytest
from fixture.db import DbFixture
from model.user import User
import ftputil

fixture = None
target = None


def install_server_configuration(host, username, password):
    with ftputil.FTPHost(host, username, password) as remote:
        if remote.path.isfile("config_inc.php.bak"):
            remote.remove("config_inc.php.bak")
        if remote.path.isfile("config_inc.php"):
            remote.rename("config_inc.php", "config_inc.php.bak")
        remote.upload(os.path.join(os.path.dirname(__file__), "resources/config_inc.php"), "config_inc.php")


def restore_server_configuration(host, username, password):
    with ftputil.FTPHost(host, username, password) as remote:
        if remote.path.isfile("config_inc.php.bak"):
            if remote.path.isfile("config_inc.php"):
                remote.remove("config_inc.php")
            remote.rename("config_inc.php.bak", "config_inc.php")


def load_config(file):
    global target
    if target is None:
        config_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), file)
        with open(config_file) as file:
            target = json.load(file)
    return target


@pytest.fixture(scope="session")
def config(request):
    return load_config(request.config.getoption("--target"))


@pytest.fixture
def app(request, config):
    global fixture
    if fixture is None or not fixture.is_valid():
        fixture = Application(browser=config["web"]["browser"], config=config)
        fixture.session.ensure_login(User(username=config["adminweb"]["user"],
                                          password=config["adminweb"]["password"]))
    return fixture


@pytest.fixture(scope="session", autouse=True)
def configure_server(request, config):
    install_server_configuration(config["ftp"]["host"], config["ftp"]["username"], config["ftp"]["password"])

    def fin():
        restore_server_configuration(config["ftp"]["host"], config["ftp"]["username"], config["ftp"]["password"])

    request.addfinalizer(fin)


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
