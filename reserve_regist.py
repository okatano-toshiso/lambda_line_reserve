import json
from datetime import datetime
from sqlalchemy.orm import sessionmaker

# models.pyからBase, LineReserve, LineUserをインポート
from models import Base, LineReserve, LineUser
# database_initializer.pyからDatabaseInitializerをインポート
from database_initializer import DatabaseInitializer
# env_variable_loader.pyからEnvVariableLoaderをインポート
from env_variable_loader import EnvVariableLoader

def handler(event, context):
    # EnvVariableLoaderクラスを使って環境変数を取得
    config_loader = EnvVariableLoader()
    db_config = config_loader.get_database_config()
    access_token = config_loader.get_access_token()

    # DatabaseInitializerクラスを使ってデータベースを初期化
    db_initializer = DatabaseInitializer(
        db_user=db_config['db_user'], 
        db_password=db_config['db_password'], 
        db_host=db_config['db_host'], 
        db_name=db_config['db_name']
    )
    
    # エラーハンドリングをDatabaseInitializer内で行う
    db_initializer.create_database_if_not_exists()

    # テーブルを作成
    db_initializer.create_tables(Base)

    # データベースに接続するエンジンを取得
    engine = db_initializer.get_engine_with_db()
    Session = sessionmaker(bind=engine)
    session = Session()

    # request datas to json
    try:
        request_body = json.loads(event['body'])
    except Exception as e:
        print(f"無効なリクエストボディ: {e}")
        return {
            'statusCode': 400,
            'body': json.dumps('Invalid request body')
        }

    # get request datas
    line_reserves_data = request_body.get('line_reserves', [])
    line_users_data = request_body.get('line_users', [])

    # put result
    response_message = ""

    try:
        for line_reserve_data in line_reserves_data:
            if line_reserve_data.get('token') != access_token:
                return {
                    'statusCode': 401,
                    'body': json.dumps('Invalid Token')
                }
            line_reserve_data.pop('token', None)
            date_fields = ['reservation_date', 'check_in', 'check_out', 'created_at', 'updated_at']
            for field in date_fields:
                if field in line_reserve_data and line_reserve_data[field]:
                    line_reserve_data[field] = datetime.strptime(line_reserve_data[field], '%Y-%m-%d')
            line_reserve = LineReserve(**line_reserve_data)
            session.add(line_reserve)

        for line_user_data in line_users_data:
            if line_user_data.get('token') != access_token:
                return {
                    'statusCode': 401,
                    'body': json.dumps('Invalid Token')
                }
            line_user_data.pop('token', None)
            date_fields = ['created_at', 'updated_at']
            for field in date_fields:
                if field in line_user_data and line_user_data[field]:
                    line_user_data[field] = datetime.strptime(line_user_data[field], '%Y-%m-%d')
            existing_user = session.query(LineUser).filter_by(
                line_id=line_user_data['line_id'],
                name=line_user_data['name'],
                phone_number=line_user_data['phone_number']
            ).first()
            if not existing_user:
                line_user = LineUser(**line_user_data)
                session.add(line_user)
        session.commit()
        response_message = "Reservations processed successfully"

    except Exception as err:
        print(f"error message: {err}")
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
