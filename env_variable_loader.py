import os

class EnvVariableLoader:
    def __init__(self):
        # 環境変数の取得
        self.db_host = os.environ.get('DB_HOST')
        self.db_user = os.environ.get('DB_USER')
        self.db_password = os.environ.get('DB_PASSWORD')
        self.db_name = os.environ.get('DB_NAME')
        self.access_token = os.environ.get('ACCESS_TOKEN')

    def get_database_config(self):
        # データベース関連の環境変数を返す
        return {
            'db_host': self.db_host,
            'db_user': self.db_user,
            'db_password': self.db_password,
            'db_name': self.db_name
        }

    def get_access_token(self):
        # アクセストークンを返す
        return self.access_token
