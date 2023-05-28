import time

from fixture.page_opener import PageOpener
from fixture.session_helper import SessionHelper
from model.project_data import ProjectData


class Project_helper:

    def __init__(self, app):
        self.app = app
        self.page_opener = PageOpener(app)
        self.session = SessionHelper(app)

    def input_text_in_field(self, text, selector_name):
        wd = self.app.wd
        field = wd.find_element_by_name(selector_name)
        field.click()
        field.clear()
        field.send_keys(text)

    def create_project(self, project_data):
        wd = self.app.wd
        self.page_opener.open_page_with_check(part_of_url="manage_proj_page.php")
        create_project_btn = wd.find_element_by_xpath("//input[@value='Create New Project']")
        create_project_btn.click()
        self.input_text_in_field(selector_name="name", text=project_data.project_name)
        if project_data.description:
            self.input_text_in_field(selector_name="name", text=project_data.description)
        wd.find_element_by_class_name("button").click()
        return ProjectData(project_name=project_data.project_name,description=project_data.description)


