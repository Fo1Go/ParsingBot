import sqlite3
from pathlib import Path
import re
import time
from selenium.webdriver.common.by import By

from bot import structures
from bot.services.ParserMixin import ParserMixin


class GoogleMailAccount(ParserMixin):
    def __init__(self, record: structures.GmailRecord):
        super().__init__()
        self._email = record.email
        self._password = record.password
        self._name = None
        self._surname = None
        self._birthdate = None
        self._reserve_email = None

        self._gmail_url = "https://mail.google.com/mail/u/0/"

    def enter_in_account(self) -> bool:
        self._driver.get(self._gmail_url)

        self.enter_data_in_element(self.get_element_by_name("identifier", 2), self._email)
        self.enter_data_in_element(self.get_element_by_name("Passwd", 5), self._password)
        time.sleep(3)
        self._save_cookies()

        return True

    def change_password(self, new_password: str) -> bool:
        if not self._cookies:
            self.enter_in_account()
        self._driver.get("https://myaccount.google.com/signinoptions/password")

        self.enter_data_in_element(self.get_element_by_name("password", 2), new_password, False)
        self.enter_data_in_element(self.get_element_by_name("confirmation_password", 2), new_password)
        self._password = new_password
        self._save_cookies()

        return True

    def change_name(self, new_name: str, new_surname: str):
        if not self._cookies:
            self.enter_in_account()
        self._driver.get("https://myaccount.google.com/profile/name")
        self._driver.get("https://myaccount.google.com/profile/name/edit")

        if new_name:
            self.enter_data_in_element(self.get_element_by_id("i7", 2), new_name, False)
            self._name = new_name
        if new_surname:
            self.enter_data_in_element(self.get_element_by_id("i12", 2), new_surname, False)
            self._name = new_surname
        self.get_save_button().click()
        return True

    def save_account_data(self):
        if not self._cookies:
            self.enter_in_account()

        file_path = Path(__file__).resolve().parent.parent.parent
        con = sqlite3.connect(file_path / "data/db/gmails.db")
        cur = con.cursor()
        cur.execute(f"INSERT INTO gmails_accounts VALUES ({self._email}, {self._password}, {self.get_fullname()}, {self._birthdate}, {self.get_reserve_email()})")
        con.commit()
        return True

    def close(self):
        self._driver.close()

    def get_birthday(self):
        if not self._cookies:
            self.enter_in_account()
        self._driver.get("https://myaccount.google.com/personal-info")
        pattern = re.compile(r"^[A-Za-z]+ \d+, \d{4}$")
        for div in self._driver.find_elements(By.TAG_NAME, "div"):
            if div.text and any(char.isdigit() for char in div.text):
                if pattern.match(div.text):
                    self._birthdate = div.text
        return self._birthdate

    def get_fullname(self):
        if not self._cookies:
            self.enter_in_account()
        self._driver.get("https://myaccount.google.com/profile/name")
        self._driver.get("https://myaccount.google.com/profile/name/edit")

        if self._name is None:
            self._name = self.get_element_by_id("i7", 2).get_property("value")
        if self._surname is None:
            self._surname = self.get_element_by_id("i12", 2).get_property("value")
        return f"{self._name} {self._surname}"

    def get_reserve_email(self):
        if not self._cookies:
            self.enter_in_account()
        self._driver.get("https://myaccount.google.com/security")
        for div in self._driver.find_elements(By.TAG_NAME, "div"):
            if div.text:
                if div.text.count("@"):
                    self._reserve_email = div.text
                    return
        self._reserve_email = "No reserve"
        return self._reserve_email

    def get_save_button(self):
        for btn in self._driver.find_elements(By.TAG_NAME, "span"):
            if btn.text.lower() == "save":
                return btn
