from dataclasses import dataclass


@dataclass
class GmailRecord:
    email: str
    password: str


@dataclass
class TwitterRecord:
    username: str
    password: str
