import json
from sqlalchemy import func
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import ProgrammingError
from sqlalchemy import and_
from utils.models import LineReserve
from utils.env_variable_loader import EnvVariableLoader
from utils.auth import get_access_token_from_header


def get_reservation(event, db_initializer):
    config_loader = EnvVariableLoader()
    access_token = config_loader.get_access_token()
    engine = db_initializer.get_engine_with_db()
    Session = sessionmaker(bind=engine)
    session = Session()

    query_params = event.get("queryStringParameters", {})
    name = query_params.get("name")
    phone_number = query_params.get("phone_number")
    line_id = query_params.get("line_id")
    reservation_id = query_params.get("reservation_id")

    headers = event.get("headers", {})
    error_response, auth_access_token = get_access_token_from_header(headers)

    if error_response:
        return error_response

    if auth_access_token != access_token:
        return {"statusCode": 401, "body": json.dumps("Invalid Token")}

    try:
        if reservation_id:
            reserves = (
                session.query(LineReserve)
                .filter(
                    and_(
                        LineReserve.name == name,
                        LineReserve.phone_number == phone_number,
                        LineReserve.line_id == line_id,
                        LineReserve.reservation_id == reservation_id,
                        LineReserve.status != "CANCEL",
                    )
                )
                .all()
            )
        else:
            reserves = (
                session.query(LineReserve)
                .filter(
                    and_(
                        LineReserve.name == name,
                        LineReserve.phone_number == phone_number,
                        LineReserve.line_id == line_id,
                        LineReserve.status != "CANCEL",
                    )
                )
                .all()
            )

        if not reserves:
            return None

        result = [reserve.as_dict() for reserve in reserves]

        return {"statusCode": 200, "body": json.dumps(result, ensure_ascii=False)}

    except Exception as e:
        print(f"Error fetching reservations: {e}")
        return {
            "statusCode": 500,
            "body": json.dumps({"message": "Internal server error"}),
        }

    finally:
        session.close()


def get_latest_reservation_id(db_initializer):
    try:
        engine = db_initializer.get_engine_with_db()
        Session = sessionmaker(bind=engine)
        session = Session()
        latest_id = session.query(func.max(LineReserve.reservation_id)).scalar()
        session.close()

        return {"statusCode": 200, "body": json.dumps({"latest_reserve_id": latest_id})}

    except ProgrammingError as e:
        print(f"Error fetching latest_reserve_id (likely missing table): {e}")
        return {"statusCode": 200, "body": json.dumps({"latest_reserve_id": 0})}

    except Exception as e:
        print(f"Error fetching latest_reserve_id: {e}")
        return {"statusCode": 500, "body": json.dumps("Internal server error")}
