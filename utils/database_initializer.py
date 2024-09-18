from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError, ProgrammingError

class DatabaseInitializer:
    def __init__(self, db_user, db_password, db_host, db_name):
        self.db_user = db_user
        self.db_password = db_password
        self.db_host = db_host
        self.db_name = db_name
        self.db_url_without_db = f'mysql+pymysql://{db_user}:{db_password}@{db_host}/?charset=utf8mb4'
        self.db_url_with_db = f'mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_name}?charset=utf8mb4'

    def create_database_if_not_exists(self):
        try:
            # Create engine without specifying a database
            engine = create_engine(self.db_url_without_db, echo=False)
            with engine.connect() as connection:
                connection.execute(text(f"CREATE DATABASE IF NOT EXISTS `{self.db_name}` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"))
            print(f"データベース {self.db_name} を確認または作成しました。")
        except (OperationalError, ProgrammingError) as err:
            print(f"データベースの作成に失敗しました: {err}")
            raise RuntimeError("Failed to create database") from err

    def get_engine_with_db(self):
        try:
            # Create engine with the specified database
            return create_engine(self.db_url_with_db, echo=False)
        except (OperationalError, ProgrammingError) as err:
            print(f"データベースへの接続に失敗しました: {err}")
            raise RuntimeError("Failed to connect to the database") from err

    def create_tables(self, Base):
        try:
            # Get engine and create tables
            engine = self.get_engine_with_db()
            Base.metadata.create_all(bind=engine)
            print("テーブルの作成に成功しました。")
        except Exception as err:
            print(f"テーブルの作成に失敗しました: {err}")
            raise RuntimeError("Failed to create tables") from err
