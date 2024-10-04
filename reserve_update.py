import json
from datetime import datetime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError

from utils.models import LineReserve, LineUser
from utils.env_variable_loader import EnvVariableLoader
from utils.database_initializer import DatabaseInitializer
from utils.request_parser import RequestParser
from utils.validator import Validator
from utils.auth import get_access_token_from_header


def handler(event, context, db_initializer):
    config_loader = EnvVariableLoader()
    access_token = config_loader.get_access_token()

    engine = db_initializer.get_engine_with_db()
    Session = sessionmaker(bind=engine)
    session = Session()

    request_parser = RequestParser()
    request_body = request_parser.parse_request_body(event)

    try:
        for line_reserve_data in request_body.get('line_reserves', []):
            Validator.validate_data(line_reserve_data, 'line_reserves')
        for line_user_data in request_body.get('line_users', []):
            Validator.validate_data(line_user_data, 'line_users')
    except ValueError as e:
        return {
            'statusCode': 400,
            'body': json.dumps(f'Validation error: {str(e)}')
        }

    headers = event.get('headers', {})
    error_response, auth_access_token = get_access_token_from_header(headers)

    if error_response:
        return error_response

    if auth_access_token != access_token:
        return {
            'statusCode': 401,
            'body': json.dumps('Invalid Token')
        }

    line_reserves_data = request_body.get('line_reserves', [])
    line_users_data = request_body.get('line_users', [])
    response_message = ""
    not_found_records = []

    try:

        for line_reserve_data in line_reserves_data:
            date_fields = ['reservation_date', 'check_in', 'check_out']
            for field in date_fields:
                if field in line_reserve_data and line_reserve_data[field]:
                    line_reserve_data[field] = datetime.strptime(line_reserve_data[field], '%Y-%m-%d')
            datetime_fields = ['created_at', 'updated_at']
            for field in datetime_fields:
                if field in line_reserve_data and line_reserve_data[field]:
                    line_reserve_data[field] = datetime.strptime(line_reserve_data[field], '%Y-%m-%d %H:%M:%S')
            existing_reserve = session.query(LineReserve).filter_by(
                id=line_reserve_data['id'],
                reservation_id=line_reserve_data['reservation_id']
            ).first()
            if existing_reserve:
                line_reserve = LineReserve(**line_reserve_data)
                session.merge(line_reserve)
            else:
                not_found_records.append({
                    "type": "LineReserve",
                    "id": line_reserve_data['id'],
                    "reservation_id": line_reserve_data['reservation_id'],
                    "message": "Reservation data not found."
                })

        for line_user_data in line_users_data:
            datetime_fields = ['created_at', 'updated_at']
            for field in datetime_fields:
                if field in line_user_data and line_user_data[field]:
                    line_user_data[field] = datetime.strptime(line_user_data[field], '%Y-%m-%d %H:%M:%S')
            if 'new_name' in line_user_data:
                line_user_data['name'] = line_user_data['new_name']
            if 'new_phone_number' in line_user_data:
                line_user_data['phone_number'] = line_user_data['new_phone_number']
            existing_user = session.query(LineUser).filter_by(
                line_id=line_user_data['line_id'],
                name=line_user_data['name'],
                phone_number=line_user_data['phone_number']
            ).first()
            if existing_user is not None:
                print('existing_user',existing_user)
                if 'new_name' in line_user_data:
                    existing_user.name = line_user_data['new_name']
                if 'new_phone_number' in line_user_data:
                    existing_user.phone_number = line_user_data['new_phone_number']
                session.merge(existing_user)
            else:
                if isinstance(line_user_data, dict) and 'new_name' in line_user_data:
                    del line_user_data['new_name']
                if isinstance(line_user_data, dict) and 'new_phone_number' in line_user_data:
                    del line_user_data['new_phone_number']

                new_user = LineUser(**line_user_data)
                session.add(new_user)

        if not_found_records:
            session.rollback()
            return {
                'statusCode': 404,
                'body': json.dumps({
                    'message': "Some records were not found.",
                    'not_found_records': not_found_records
                }, ensure_ascii=False)
            }
        session.commit()
        response_message = "Reservations and users updated successfully"

    except SQLAlchemyError as err:
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
