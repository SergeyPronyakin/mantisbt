from fixture.generator_helper import GeneratorHelper
from model.project_data import ProjectData
from model.user import User


def test_create_project(app):
    admin_data = User(username=app.config["adminweb"]["user"], password=app.config["adminweb"]["password"])
    old_projects = app.soap.get_projects(admin_data.username, admin_data.password)
    created_project = app.project.create_project(ProjectData(project_name=GeneratorHelper().random_str("project", 10), description="sdsd"))
    actual_projects = app.soap.get_projects(admin_data.username, admin_data.password)
    old_projects.append(created_project)
    assert sorted(old_projects, key=ProjectData.id_or_max) == sorted(actual_projects, key=ProjectData.id_or_max)


def test_delete_project(app):
    if app.project.get_projects_data() == 0:
        app.project.create_project(
            ProjectData(project_name=GeneratorHelper().random_str("project", 10)))

    old_projects = app.soap.get_projects()
    deleted_project = app.project.delete_first_project()
    actual_projects = app.soap.get_projects(username=app.config["adminweb"]["user"], password=app.config["adminweb"]["password"])
    actual_projects.append(deleted_project)
    assert sorted(old_projects, key=ProjectData.id_or_max) == sorted(actual_projects, key=ProjectData.id_or_max)


def test_signup_new_account(app):
    username = GeneratorHelper().random_str("User_name", 10)
    password = "test"
    email = username + "@localhost"
    app.james.insure_user_exist(username, password)
    app.signup.new_user(username, email, password)
    assert app.soap.can_login(username, password)


