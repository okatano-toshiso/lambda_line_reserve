import json
from datetime import datetime
from sqlalchemy.orm import sessionmaker

from utils.models import Base, LineReserve, LineUser
from utils.env_variable_loader import EnvVariableLoader
from utils.database_initializer import DatabaseInitializer
from utils.request_parser import RequestParser

def handler(event, context):
    config_loader = EnvVariableLoader()
    db_config = config_loader.get_database_config()
    access_token = config_loader.get_access_token()

    db_initializer = DatabaseInitializer(
        db_user=db_config['db_user'],
        db_password=db_config['db_password'],
        db_host=db_config['db_host'],
        db_name=db_config['db_name']
    )

    db_initializer.create_database_if_not_exists()
    db_initializer.create_tables(Base)

    engine = db_initializer.get_engine_with_db()
    Session = sessionmaker(bind=engine)
    session = Session()

    request_parser = RequestParser()
    try:
        request_body = request_parser.parse_request_body(event)
    except ValueError:
        return {
            'statusCode': 400,
            'body': json.dumps('Invalid request body')
        }

    line_reserves_data = request_body.get('line_reserves', [])
    line_users_data = request_body.get('line_users', [])
    response_message = ""

    try:
        for line_reserve_data in line_reserves_data:
            if line_reserve_data.get('token') != access_token:
                return {
                    'statusCode': 401,
                    'body': json.dumps('Invalid Token')
                }
            line_reserve_data.pop('token', None)

            date_fields = ['reservation_date', 'check_in', 'check_out']
            for field in date_fields:
                if field in line_reserve_data and line_reserve_data[field]:
                    line_reserve_data[field] = datetime.strptime(line_reserve_data[field], '%Y-%m-%d')

            datetime_fields = ['created_at', 'updated_at']
            for field in datetime_fields:
                if field in line_reserve_data and line_reserve_data[field]:
                    line_reserve_data[field] = datetime.strptime(line_reserve_data[field], '%Y-%m-%d %H:%M:%S')
            line_reserve = LineReserve(**line_reserve_data)
            session.add(line_reserve)

        for line_user_data in line_users_data:
            if line_user_data.get('token') != access_token:
                return {
                    'statusCode': 401,
                    'body': json.dumps('Invalid Token')
                }
            line_user_data.pop('token', None)

            datetime_fields = ['created_at', 'updated_at']
            for field in date_fields:
                if field in line_user_data and line_user_data[field]:
                    line_user_data[field] = datetime.strptime(line_user_data[field], '%Y-%m-%d %H:%M:%S')
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
        print(f"Error during reservation processing: {err}")
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
