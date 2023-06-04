from fixture.generator_helper import GeneratorHelper
from model.project_data import ProjectData


def test_create_project(app):
    old_projects = app.soap.get_projects()
    created_project = app.project.create_project(ProjectData(project_name=GeneratorHelper().random_str("Project", 10),
                                                             description="Some description"))
    actual_projects = app.soap.get_projects()
    old_projects.append(created_project)
    assert sorted(old_projects, key=ProjectData.id_or_max) == sorted(actual_projects, key=ProjectData.id_or_max)


def test_delete_project(app):
    if app.project.get_projects_data() == 0:
        app.project.create_project(
            ProjectData(project_name=GeneratorHelper().random_str("Project", 10)))

    old_projects = app.soap.get_projects()
    deleted_project = app.project.delete_first_project()
    actual_projects = app.soap.get_projects()
    actual_projects.append(deleted_project)
    assert sorted(old_projects, key=ProjectData.id_or_max) == sorted(actual_projects, key=ProjectData.id_or_max)


def test_signup_new_account(app):
    username = GeneratorHelper().random_str("User_name", 10)
    password = "test"
    email = f"{username}@localhost"
    app.james.insure_user_exist(username, password)
    app.signup.new_user(username, email, password)
    assert app.soap.can_login(username, password)
