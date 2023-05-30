from selenium import webdriver
from selenium.common.exceptions import NoAlertPresentException, NoSuchElementException

from fixture.page_opener import PageOpener
from fixture.project_helper import Project_helper
from fixture.session_helper import SessionHelper
from fixture.james_helper import JamesHelper


class Application:
    def __init__(self, browser, base_url):
        if browser == "firefox":
            self.wd = webdriver.Firefox()
        elif browser == "chrome":
            self.wd = webdriver.Chrome()
        else:
            raise ValueError("Couldn't open any browser")

        self.session = SessionHelper(self)
        self.page_opener = PageOpener(self)
        self.project = Project_helper(self)
        self.james = JamesHelper(self)
        self.base_url = base_url

    def is_valid(self):
        try:
            self.wd.current_url
            return True
        except:
            return False

    def open_main_page(self):
        wd = self.wd
        wd.get(self.base_url)
        return wd

    def current_url(self):
        wd = self.wd
        return wd.current_url

    def is_element_present(self, how, what):
        try:
            self.wd.find_element(by=how, value=what)
        except NoSuchElementException:
            return False
        return True

    def is_alert_present(self):
        try:
            self.wd.switch_to.alert()
        except NoAlertPresentException:
            return False
        return True

    def quit(self):
        self.wd.quit()
