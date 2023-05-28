import time
import re
from selenium.webdriver.common.by import By
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
            self.input_text_in_field(selector_name="description", text=project_data.description)
        wd.find_element_by_class_name("button").click()
        return ProjectData(id=project_data.id, project_name=project_data.project_name,description=project_data.description)

    def get_project_objects(self):
        wd = self.app.wd
        self.page_opener.open_page_with_check(part_of_url="manage_proj_page.php")
        return wd.find_elements_by_xpath("/html/body/table[3]/tbody/tr")[2:]

    def get_projects_data(self):
        project_data_list = []
        all_projects_data = self.get_project_objects()
        for project_data in all_projects_data:
            project_name = project_data.find_element(By.XPATH, "td[1]").text
            description = project_data.find_element(By.XPATH, "td[5]").text
            project_link = project_data.find_element(By.TAG_NAME, "a").get_attribute('href')
            id = re.search("id=([^\n]+)", project_link).group(0)[3:]
            project_data_list.append(ProjectData(id=id, project_name=project_name, description=description))
        return project_data_list


