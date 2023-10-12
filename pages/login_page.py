from pages.base_page import BasePage
from locators.login_page_locator import LoginPageLocator


class LoginPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.locator = LoginPageLocator
        self.open('/login')

    def get_login_form_label(self):
        return self.find_element(*self.locator.lbl_login_form).text

    def get_expected_error_message(self):
        return self.find_element(*self.locator.lbl_error_message).text

    def login(self, email: str, password: str):
        # STEPS
        # Fill email
        self._driver.find_element(*self.locator.txt_email).send_keys(email)
        self.sleep(1)

        # Fill password
        self._driver.find_element(*self.locator.txt_password).send_keys(password)
        self.sleep(1)

        # Click login button
        self._driver.find_element(*self.locator.btn_submit).click()
        self.sleep()
