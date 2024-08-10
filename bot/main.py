import random
import string

from structures import GmailRecord, TwitterRecord
from services.google_mail import GoogleMailAccount
from services.twitter import TwitterAccount


if __name__ == "__main__":
    mail = GoogleMailAccount(GmailRecord(email="email", password="pass"))
    x = TwitterAccount(TwitterRecord(username="username", password="pass"))
    try:
        mail.save_account_data()
        x.post_twitter(''.join(random.choices(string.ascii_letters + string.digits, k=10)))
    finally:
        mail.close()
