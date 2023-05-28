from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait


class SessionHelper:

    def __init__(self, app):
        self.app = app

    def login(self, userdata):
        wd = self.app.wd
        self.app.open_main_page()
        WebDriverWait(wd, 20).until(EC.presence_of_element_located((By.NAME, "username")))
        username_field = wd.find_element_by_name("username")
        username_field.clear()
        username_field.send_keys(userdata.username)
        wd.find_element_by_name("password").click()
        wd.find_element_by_name("password").clear()
        wd.find_element_by_name("password").send_keys(userdata.password)
        wd.find_element_by_xpath("//input[@value='Login']").click()

    def logout(self):
        wd = self.app.wd
        WebDriverWait(wd, 20).until(EC.presence_of_element_located((By.LINK_TEXT, 'Logout'))).click()
        WebDriverWait(wd, 20).until(EC.presence_of_element_located((By.XPATH, "//input[@value='Login']")))

    def ensure_logout(self):
        if self.is_logged_in():
            self.logout()

    def is_logged_in(self):
        wd = self.app.wd
        return len(wd.find_elements_by_link_text("Logout")) > 0

    def is_logged_in_as(self, username):
        wd = self.app.wd
        return wd.find_element_by_xpath("//div/div[1]/form/b").text == "(" + username + ")"

    def ensure_login(self, userdata):
        if self.is_logged_in():
            if self.is_logged_in_as(userdata.username):
                return
            else:
                self.logout()
        self.login(userdata)
