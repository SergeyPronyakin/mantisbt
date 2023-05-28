from fixture.generator_helper import GeneratorHelper
from model.project_data import ProjectData


def test_login(app):
    app.session.login("administrator", "root")
    assert app.session.is_logged_in_as("administrator")


def test_create_project(app):
    old_projects = app.project.get_projects_data()
    created_project = app.project.create_project(ProjectData(project_name=GeneratorHelper().random_str("project", 10), description="sdsd"))
    actual_projects = app.project.get_projects_data()
    old_projects.append(created_project)

    assert sorted(old_projects, key=ProjectData.id_or_max) == sorted(actual_projects, key=ProjectData.id_or_max)


def test_delete_project(app):
    if app.project.get_projects_data() == 0:
        app.project.create_project(
            ProjectData(project_name=GeneratorHelper().random_str("project", 10)))

    old_projects = app.project.get_projects_data()
    deleted_project = app.project.delete_first_project()
    new_projects = app.project.get_projects_data()

    new_projects.append(deleted_project)

    assert sorted(old_projects, key=ProjectData.id_or_max) == sorted(new_projects, key=ProjectData.id_or_max)
