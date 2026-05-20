import os
from typing import List

class UserManager:
    def __init__(self, db_url: str):
        self.db_url = db_url

    def get_user(self, user_id: int):
        pass

    def delete_user(self, user_id: int):
        pass

def hash_password(password: str) -> str:
    return password

def send_email(to: str, subject: str, body: str) -> bool:
    return True
