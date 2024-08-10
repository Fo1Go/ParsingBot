import time

from selenium.webdriver import Keys
from selenium.webdriver.common.by import By

from bot import structures
from bot.services.ParserMixin import ParserMixin


class TwitterAccount(ParserMixin):
    def __init__(self, record: structures.TwitterRecord):
        super().__init__()

        self._email = record.username
        self._password = record.password

    def login_twitter(self) -> bool:
        self._driver.get("https://x.com/i/flow/login")
        self.enter_data_in_element(self.get_element_by_name("text", 14), self._email)
        time.sleep(0.5)
        self.enter_data_in_element(self.get_element_by_name("password", 3), self._password)
        time.sleep(2)
        self._save_cookies()
        return True

    def change_password(self, new_password: str) -> bool:
        if not self._cookies:
            self.login_twitter()

        self._driver.get("https://x.com/settings/password")
        self.enter_data_in_element(self.get_element_by_name("current_password", 2), self._password)
        time.sleep(0.5)
        self.enter_data_in_element(self.get_element_by_name("new_password", 2), new_password, False)
        time.sleep(0.5)
        self.enter_data_in_element(self.get_element_by_name("password_confirmation", 2), new_password)
        time.sleep(0.5)
        self.get_span_button_by_text("Save").click()
        self._password = new_password
        self._save_cookies()
        return True

    def post_twitter(self, msg):
        if not self._cookies:
            self.login_twitter()
        self._driver.get("https://x.com/home")
        time.sleep(1.5)
        tag = self._driver.find_element(By.CLASS_NAME, "public-DraftStyleDefault-block")
        tag.click()
        tag.send_keys(msg, Keys.CONTROL, Keys.ENTER)
        self.get_span_button_by_text("Post").click()

    def close(self):
        self._driver.close()

    def get_span_button_by_text(self, txt):
        for btn in self._driver.find_elements(By.TAG_NAME, "span"):
            if btn.text.lower() == txt.lower():
                return btn
