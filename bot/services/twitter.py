from tests import structures
import selenium
import sqlite3


class TwitterAccount:
    def __init__(self, record: structures.GmailRecord):
        self._email = record.email
        self._password = record.password

    def is_account_exists(self) -> bool:
        #        - Twitter должен быть создан ранее!
        ...

    def change_password(self):
        #         - Изменение пароля
        ...

    def verify_mail(self):
        #        - Подтверждение через почту/указание резервной почты
        ...

    def post_twitter(self):
#         - Сделать рандомный пост в Twitter (со звездочкой написать через chatGTP)
        ...
