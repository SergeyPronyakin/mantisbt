from suds import WebFault
from suds.client import Client

from fixture.session_helper import SessionHelper
from model.project_data import ProjectData
from model.user import User


class SoapHelper:

    def __init__(self, app):
        self.app = app

    def can_login(self, username, password):
        client = Client("http://localhost/mantisbt-1.2.20/api/soap/mantisconnect.php?wsdl")
        try:
            response = client.service.mc_login(username, password)
            print(response)
            return True
        except WebFault:
            return False

    def get_projects(self,username, password):
        client = Client("http://localhost/mantisbt-1.2.20/api/soap/mantisconnect.php?wsdl")
        try:
            projects = client.service.mc_projects_get_user_accessible(username, password)
            project_list = []
            for project in projects:
                id = project["id"]
                name = project["name"]
                description = project["description"]
                project_list.append(ProjectData(id=id, project_name=name, description=description))
            return project_list

        except WebFault:
            return False
