import os


class EnvVariableLoader:
    def __init__(self):
        self.db_host = os.environ.get("DB_HOST")
        self.db_user = os.environ.get("DB_USER")
        self.db_password = os.environ.get("DB_PASSWORD")
        self.db_name = os.environ.get("DB_NAME")
        self.access_token = os.environ.get("ACCESS_TOKEN")

    def get_database_config(self):
        return {
            "db_host": self.db_host,
            "db_user": self.db_user,
            "db_password": self.db_password,
            "db_name": self.db_name,
        }

    def get_access_token(self):
        return self.access_token
