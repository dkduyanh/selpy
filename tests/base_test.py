import os
import unittest
import yaml
import sys

sys.path.insert(0, '../')

from selenium.webdriver.remote.webdriver import WebDriver
from selenium import webdriver


class BaseTest(unittest.TestCase):
    _config = None
    _driver: WebDriver = None
    _page = None
    _page_title: str = None
    _page_url: str = None

    @classmethod
    def setUpClass(cls) -> None:
        """
        Hook method for setting up class fixture before running tests in the class.
        :return:
        """
        cls._setup_config()
        cls._setup_driver()

    @classmethod
    def _setup_config(cls) -> None:
        """
        Load test configurations
        :return: None
        """
        cfg_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config.yml")
        if not os.path.isfile(cfg_path):
            with open(cfg_path, 'w') as file:
                cls._config = {
                    'base_url': 'https://automationexercise.com',
                    'browser': 'chrome',
                    'maximize_window': True,
                    'wait': 5,
                    'timeout': 30}
                yaml.safe_dump(cls._config, file)
        else:
            with open(cfg_path, 'r') as file:
                cls._config = yaml.safe_load(file)

    @classmethod
    def _setup_driver(cls) -> None:
        """
        Setup web driver
        :return:
        """
        match cls._config['browser']:
            case 'edge':
                edge_options = webdriver.EdgeOptions()
                cls._driver = webdriver.Edge(options=edge_options)
            case 'firefox':
                firefox_opts = webdriver.FirefoxOptions()
                cls._driver = webdriver.Firefox(options=firefox_opts)
            case 'chrome':
                chrome_opts = webdriver.ChromeOptions()
                chrome_opts.add_experimental_option("detach", True)
                cls._driver = webdriver.Chrome(options=chrome_opts)
            case default:
                raise Exception(f"'{cls._config['browser']}' is not supported browser.")

    @classmethod
    def tearDownClass(cls) -> None:
        """
        Hook method for deconstructing the class fixture after running all tests in the class.
        :return: None
        """
        cls._driver.quit()
