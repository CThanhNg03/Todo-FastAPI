import os
import dotenv

class Env:
    def __init__(self):
        dotenv.load_dotenv()
        self.host = {
            "dev": os.getenv("DEV_URL")
            # "prod": os.getenv("PROD_HOST")
        }
        self.database = {
            "url": os.getenv("DATABASE_URL")
        }
        self.secret = {
            "key": os.getenv("SECRET_KEY"),
            "algorithm": os.getenv("ALGORITHM"),
            "access_token_expire_minutes": int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
        }
        self.mail = {
            "username": os.getenv("MAIL_USERNAME"),
            "password": os.getenv("MAIL_PASSWORD"),
            "from": os.getenv("MAIL_FROM"),
            "server": os.getenv("MAIL_SERVER"),
            "from_name": "TODO APP"
        }

env = Env()