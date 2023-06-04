from suds import WebFault
from suds.client import Client
from model.project_data import ProjectData
import urllib.parse
from model.user import User


class SoapHelper:

    def __init__(self, app):
        self.app = app

    def can_login(self, username, password):
        client = Client(self.soap_url())
        try:
            response = client.service.mc_login(username, password)
            print(response)
            return True
        except WebFault:
            return False

    def get_projects(self):
        client = Client(self.soap_url())
        try:
            projects = client.service.mc_projects_get_user_accessible(self.admin_creds().username,
                                                                      self.admin_creds().password)
            return [ProjectData(id=project["id"], project_name=project["name"], description=project["description"])for project in projects]
        except WebFault:
            return False

    def admin_creds(self):
        return User(username=self.app.config["adminweb"]["user"], password=self.app.config["adminweb"]["password"])

    def soap_url(self):
        return urllib.parse.urljoin(self.app.config["web"]["baseUrl"], "api/soap/mantisconnect.php?wsdl")
