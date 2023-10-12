from selenium.webdriver.common.by import By


class LoginPageLocator(object):
    lbl_login_form = (By.XPATH, '//div[@class="login-form"]/h2')
    txt_email = (By.XPATH, '//form[@action="/login"]/input[@name="email"]')
    txt_password = (By.XPATH, '//form[@action="/login"]/input[@name="password"]')
    btn_submit = (By.XPATH, '//form[@action="/login"]/button[@type="submit"]')
    lbl_error_message = (By.XPATH, '//form[@action="/login"]/p[@style="color: red;"]')
