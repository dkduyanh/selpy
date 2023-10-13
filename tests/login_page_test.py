from tests.base_test import BaseTest
from pages.login_page import LoginPage
import unittest


class LoginPageTest(BaseTest):

    def setUp(self):
        self._page = LoginPage(self._driver, self._config)

    """
    Test Case 03: Login User with incorrect email and password
    """
    def test_login_with_incorrect_credentials(self):
        # Verify 'Login to your account' is visible
        assert self._page.get_login_form_label() == 'Login to your account'

        # Enter incorrect email address and password then click 'Login'
        email = 'my@domain.example'
        password = '123abc'
        self._page.login(email, password)

        # Verify error 'Your email or password is incorrect!' is visible
        expected_error_msg = self._page.get_expected_error_message()
        assert expected_error_msg == 'Your email or password is incorrect!'

        # save screenshot
        self._page.save_screenshot()


if __name__ == '__main__':
    unittest.main()
