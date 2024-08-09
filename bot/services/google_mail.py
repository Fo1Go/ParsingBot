from tests import structures
import selenium
import sqlite3


class GoogleMailAccount:
    def __init__(self, record: structures.GoogleRecord):
        self._email = record.email
        self._password = record.password

    def is_account_exists(self) -> bool:
        #     - Google Почта должна быть ранее создана!
        ...

    def change_password(self):
        #     - Изменить пароль.
        ...

    def change_name(self):
        #     - Изменить  Имя и Фамилию.
        ...

    def save_account_data(self):
#     - Сохранение данных в таблицу – Емейл, пароль, Имя фамилия, дата рождения, резервный емейл.
        ...
