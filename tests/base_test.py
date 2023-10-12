import os
import unittest
import yaml
import sys

sys.path.insert(0, '../')

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver import Chrome, Edge, Firefox
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions


class BaseTest(unittest.TestCase):
    _config = None
    _driver: WebDriver = None
    _page = None
    _page_title = None
    _page_url = None

    @classmethod
    def setUpClass(cls):
        cls._setup_config()
        cls._setup_driver()

    @classmethod
    def _setup_config(cls):
        # Load test configurations
        with open(os.path.dirname(os.path.dirname(__file__)) + os.path.sep + "config.yml", 'r') as ymlfile:
            cls._config = yaml.safe_load(ymlfile)

    @classmethod
    def _setup_driver(cls):
        match cls._config['browser']:
            case 'edge':
                edge_options = EdgeOptions()
                cls._driver = Edge(options=edge_options)
            case 'firefox':
                firefox_opts = FirefoxOptions()
                cls._driver = Firefox(options=firefox_opts)
            case 'chrome':
                chrome_opts = ChromeOptions()
                chrome_opts.add_experimental_option("detach", True)
                cls._driver = Chrome(options=chrome_opts)
            case default:
                raise Exception(f"'{cls._config['browser']}' is not supported browser.")

    @classmethod
    def tearDownClass(cls):
        cls._driver.quit()

