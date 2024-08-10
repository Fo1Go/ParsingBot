from selenium.common import TimeoutException
from selenium.webdriver.chrome import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from fake_useragent import UserAgent


class ParserMixin(object):
    def __init__(self):

        options = Options()
        options.add_argument("user-agent=" + UserAgent().random)
        options.add_argument("page_load_strategy=eager")
        # options.add_argument("--headless")
        # options.add_argument('--disable-gpu')
        options.add_argument('--disable-logging')
        options.add_argument('--disable-extensions')
        options.add_argument('--disable-infobars')
        options.add_argument('--disable-blink-features=AutomationControlled')
        # options.add_argument('--proxy-server=%s' % 'your-mobile-proxy:port')
        self._driver = webdriver.Chrome(options=options, keep_alive=True)
        self._save_cookies()

    def get_element(self, func, delay):
        try:
            element = self._wait_for(delay).until(func)
            if element is None:
                raise ValueError("No such element")
            return element
        except TimeoutException:
            print("Timeout")
            return None

    def get_element_by_name(self, elem: str, delay=1) -> WebElement:
        return self.get_element(EC.element_to_be_clickable((By.NAME, elem)), delay)

    def get_element_by_id(self, identification: str, delay=1) -> WebElement:
        return self.get_element(EC.element_to_be_clickable((By.ID, identification)), delay)

    def _wait_for(self, delay=1):
        return WebDriverWait(self._driver, delay)

    def _save_cookies(self):
        self._cookies = self._driver.get_cookies()

    def enter_data_in_element(self, element, text, send=True):
        if element is None:
            raise ValueError("Element is None")
        element.clear()
        element.send_keys(text)
        if send:
            element.send_keys(Keys.RETURN)
