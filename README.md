# selpy
A sample project template for automation test, based on Selenium and Python using Page-Object-Model (POM) pattern.

## Directory Structure

``` 
drivers                contains web drivers of which browsers we want to execute the tests on 
helpers                contains helper classes using in the project 
locators               contains locators of elements (DOM elements)               
pages                  contains set of page classes and methods will be used in the tests
reports                contains report data generated by the tests       
tests                  contains set of test classes that implement and execute the test cases
config.yml             contains the configurations that lets you customize to setup the project 
config.yml.example     is an example of `config.yml`
requirements.txt       is a config file for installing packages that required in the project
```

## Setup 
1. Download the project or clone repository.
2. Install packages.
    ```shell
    pip install -r requirements.txt
    ```
3. Setup configurations.
   
   We can quickly create a new `config.yml` by copying from `config.yml.example` in the root directory.
   ```shell
   cp config.yml.example config.yml
   ```

   
## Create a new test
For example, we have a test case that need to be executed automatically on Chrome browser as below:
```text
Test Case 03: Login User with incorrect email and password
    1. Launch browser
    2. Navigate to url 'https://automationexercise.com/login'
    3. Verify 'Login to your account' is visible
    4. Enter incorrect email address and password
    5. Click 'login' button
    6. Verify error 'Your email or password is incorrect!' is visible
```
1. Configure the project in the `config.yml` file in project root.
   ```yaml
   base_url: https://automationexercise.com
   browser: chrome
   wait: 5
   timeout: 10
   ```

2. Create a new class that represents for a web page we want to test in the `pages` directory.

   ```python
   # ./pages/login_page.py
   from pages.base_page import BasePage
   
   class LoginPage(BasePage):
        pass
   ```

   >    **Note:**
   >    The page class must extend the `BasePage` class.

3. Defines locators of DOM elements in `locators` directory.

   ```python
   # ./locators/login_page_locator.py
   from selenium.webdriver.common.by import By

   class LoginPageLocator(object):
       lbl_login_form = (By.XPATH, '//div[@class="login-form"]/h2')
       txt_email = (By.XPATH, '//form[@action="/login"]/input[@name="email"]')
       txt_password = (By.XPATH, '//form[@action="/login"]/input[@name="password"]')
       btn_submit = (By.XPATH, '//form[@action="/login"]/button[@type="submit"]')
       lbl_error_message = (By.XPATH, '//form[@action="/login"]/p[@style="color: red;"]')
   ```

   > **Tip:**    
   > - It's recommended to group the locators of web elements in classes so that we can reuse them by class inheritance.
   > - We can organize the locator classes by many ways such as separated web pages (i.e `login_page_locator.py`) or sections (i.e `header_locator.py`, `footer_locator.py`)

4. Add methods to page class using for the tests.
   ```python
   # ./pages/login_page.py
   from pages.base_page import BasePage
   from locators.login_page_locator import LoginPageLocator

   class LoginPage(BasePage):
       def __init__(self, driver):
           super().__init__(driver)
           self.locator = LoginPageLocator
           self.open('/login')
   
       def get_login_form_label(self):
           return self.find_element(*self.locator.lbl_login_form).text
   
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
   ```

5. Create a test class that implements the test case in `tests` directory.

   ```python
   # ./tests/login_page_test.py
   from tests.base_test import BaseTest
   from pages.login_page import LoginPage

   class LoginPageTest(BaseTest):

       def setUp(self):
           self._page = LoginPage(self._driver)
   
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
   ```

   >    **Note:**
   >    The page class should extend the `BaseTest` class.



## Execute the tests
### Using Unittest
```shell
python -m unittest tests/login_page_test.py
```

### Using Pytest
```
python -m pytest tests/login_page_test.py
```

### Using Pycharm
First, We need to set a default test runner in Pycharm:
```text
(Menu) File > Settings > Tools > Python Integrated Tools > Testing
```
Second, select one of the tests from `tests` directory and click "Run" or press `Shift + F10`

## Documentations
- [Selenium with Python](https://selenium-python.readthedocs.io/index.html)
- [WebDriver](https://www.selenium.dev/documentation/webdriver/)
- [Locator strategies](https://www.selenium.dev/documentation/webdriver/elements/locators/)
- [Page object models](https://www.selenium.dev/documentation/test_practices/encouraged/page_object_models/)
- [unittest — Unit testing framework](https://docs.python.org/3/library/unittest.html)
