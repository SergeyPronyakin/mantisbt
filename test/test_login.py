import time

from model.project_data import ProjectData


def test_login(app):
    app.session.login("administrator", "root")
    assert app.session.is_logged_in_as("administrator")


def test_create_project(app):
    app.project.create_project(ProjectData(project_name="TEST"))
