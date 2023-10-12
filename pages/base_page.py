from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
import time
import re
import os


class BasePage:
    _driver: WebDriver = None
    _base_url: str = None
    _wait: int = None
    _waiter: WebDriverWait = None
    _timeout: int = 0
    _maximize_window: bool = True

    def __init__(self, driver: WebDriver, wait: int = 1, base_url: str = 'https://automationexercise.com'):
        self._driver = driver
        self._wait = wait
        self._base_url = base_url

        if self._wait > 0:
            self._waiter = WebDriverWait(self._driver, wait)

        if self._timeout > 0:
            self._driver.set_page_load_timeout(self._timeout)

        if self._maximize_window:
            self._driver.maximize_window()

        self.sleep()

    def _get_driver(self) -> WebDriver:
        return self._driver

    def set_base_url(self, base_url) -> None:
        self._base_url = base_url

    def get_base_url(self) -> str:
        return self._base_url

    def open(self, url) -> None:
        self._driver.get(self._base_url + url)

    def close(self) -> None:
        self._driver.close()

    def quit(self) -> None:
        self._driver.quit()

    def get_url(self) -> str:
        return self._driver.current_url

    def get_title(self) -> str:
        return self._driver.title

    def sleep(self, seconds: int = 0) -> None:
        time.sleep(seconds if seconds > 0 else self._wait)

    def save_screenshot(self, filename=None) -> None:
        if not filename:
            filename = self.__class__.__name__

        # check reports dir
        reports_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'reports')
        if not os.path.exists(reports_dir):
            raise NotADirectoryError("{} does not exists" % reports_dir)

        # create screenshots dir if not exists
        screenshots_dir = os.path.join(reports_dir, 'screenshots')
        if not os.path.exists(screenshots_dir):
            os.makedirs(screenshots_dir)

        name, ext = os.path.splitext(filename)
        if not ext:
            ext = '.png'
            filename = name + ext
        counter = 0

        file_path = os.path.join(screenshots_dir, filename)
        while os.path.isfile(file_path):
            counter += 1
            filename = name + (" (%d)" % counter) + ext
            file_path = os.path.join(screenshots_dir, filename)

        self._driver.save_screenshot(file_path)

    def find_element(self, *locator) -> WebElement:
        return self._driver.find_element(*locator)

    def find_elements(self, *locator) -> [WebElement]:
        return self._driver.find_elements(*locator)

    def scroll_to_element(self, element: WebElement):
        self._driver.execute_script("arguments[0].scrollIntoView();", element)

    def scroll_to_bottom_of_page(self, interval: int = 2) -> None:
        height = self._driver.execute_script("return document.body.scrollHeight")
        while True:
            # Scroll down to the bottom.
            self._driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            # Wait to load the page.
            time.sleep(interval if interval > 0 else 2)
            # Calculate new scroll height and compare with last scroll height.
            new_height = self._driver.execute_script("return document.body.scrollHeight")
            if new_height == height:
                break
            height = new_height

    def scroll_to_top_of_page(self) -> None:
        self._driver.execute_script("window.scrollTo(0, 0);")
