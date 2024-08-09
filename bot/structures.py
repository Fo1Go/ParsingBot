from dataclasses import dataclass


class GmailRecord(dataclass):
    email: str
    password: str


class TwitterRecord(dataclass):
    email: str
    password: str
