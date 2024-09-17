# def handler(event, context):
#     # 予約登録のロジック
#     return {
#         'statusCode': 200,
#         'body': '予約を正常に登録させる処理を書くよ。ヌルぽっ'
#     }

import json
import os
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, Date, DateTime, Boolean, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError, ProgrammingError

Base = declarative_base()

# モデルの定義
class LineReserve(Base):
    __tablename__ = 'line_reserves'

    id = Column(Integer, primary_key=True, autoincrement=True)
    reservation_id = Column(Integer)
    reservation_date = Column(Date)
    check_in = Column(Date)
    check_out = Column(Date)
    line_id = Column(String(255))
    name = Column(String(255))
    phone_number = Column(String(20))
    status = Column(String(50))
    count_of_person = Column(Integer)
    room_type = Column(String(50))
    option_id = Column(Integer)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

class LineUser(Base):
    __tablename__ = 'line_users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    line_id = Column(String(255))
    name = Column(String(255))
    name_kana = Column(String(255))
    phone_number = Column(String(20))
    age = Column(Integer)
    adult = Column(Boolean)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

def handler(event, context):
    # 環境変数の取得
    db_host = os.environ['DB_HOST']
    db_user = os.environ['DB_USER']
    db_password = os.environ['DB_PASSWORD']
    db_name = os.environ['DB_NAME']
    ACCESS_TOKEN = os.environ['ACCESS_TOKEN']

    # 1. データベース名を指定せずにエンジンを作成
    db_url_without_db = f'mysql+pymysql://{db_user}:{db_password}@{db_host}/?charset=utf8mb4'
    engine = create_engine(db_url_without_db, echo=False)

    # データベースの作成
    try:
        with engine.connect() as connection:
            connection.execute(text(f"CREATE DATABASE IF NOT EXISTS `{db_name}` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"))
    except (OperationalError, ProgrammingError) as err:
        print(f"データベースの作成に失敗しました: {err}")
        return {
            'statusCode': 500,
            'body': json.dumps('Internal server error')
        }

    # 2. データベース名を指定してエンジンとセッションを再作成
    db_url_with_db = f'mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_name}?charset=utf8mb4'
    engine = create_engine(db_url_with_db, echo=False)
    Session = sessionmaker(bind=engine)
    session = Session()

    # テーブルの作成
    try:
        Base.metadata.create_all(bind=engine)
    except Exception as err:
        print(f"テーブルの作成に失敗しました: {err}")
        return {
            'statusCode': 500,
            'body': json.dumps('Internal server error')
        }

    # リクエストボディの取得とパース
    try:
        request_body = json.loads(event['body'])
    except Exception as e:
        print(f"無効なリクエストボディ: {e}")
        return {
            'statusCode': 400,
            'body': json.dumps('Invalid request body')
        }

    # リクエストデータの取得
    line_reserves_data = request_body.get('line_reserves', [])
    line_users_data = request_body.get('line_users', [])

    print("line_reserves_data")
    print(line_reserves_data)

    print("line_users_data")
    print(line_users_data)

    # 処理結果の格納用
    response_message = ""

    try:
        # LineReserveの処理
        for line_reserve_data in line_reserves_data:
            if line_reserve_data.get('token') != ACCESS_TOKEN:
                return {
                    'statusCode': 401,
                    'body': json.dumps('Invalid Token')
                }

            # tokenを削除
            line_reserve_data.pop('token', None)

            # 日付フィールドの変換
            date_fields = ['reservation_date', 'check_in', 'check_out', 'created_at', 'updated_at']
            for field in date_fields:
                if field in line_reserve_data and line_reserve_data[field]:
                    line_reserve_data[field] = datetime.strptime(line_reserve_data[field], '%Y-%m-%d')

            # LineReserveオブジェクトの作成
            line_reserve = LineReserve(**line_reserve_data)
            session.add(line_reserve)

        # LineUserの処理
        for line_user_data in line_users_data:
            if line_user_data.get('token') != ACCESS_TOKEN:
                return {
                    'statusCode': 401,
                    'body': json.dumps('Invalid Token')
                }

            # tokenを削除
            line_user_data.pop('token', None)

            # 日付フィールドの変換
            date_fields = ['created_at', 'updated_at']
            for field in date_fields:
                if field in line_user_data and line_user_data[field]:
                    line_user_data[field] = datetime.strptime(line_user_data[field], '%Y-%m-%d')

            # ユーザーの存在確認
            existing_user = session.query(LineUser).filter_by(
                line_id=line_user_data['line_id'],
                name=line_user_data['name'],
                phone_number=line_user_data['phone_number']
            ).first()

            if not existing_user:
                line_user = LineUser(**line_user_data)
                session.add(line_user)

        # 変更のコミット
        session.commit()
        response_message = "Reservations processed successfully"

    except Exception as err:
        print(f"予約処理中のエラー: {err}")
        session.rollback()
        return {
            'statusCode': 500,
            'body': json.dumps('Internal server error')
        }
    finally:
        session.close()

    return {
        'statusCode': 200,
        'body': json.dumps({'message': response_message}, ensure_ascii=False)
    }
