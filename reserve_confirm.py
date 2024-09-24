import json
from sqlalchemy import func
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import ProgrammingError
from utils.models import LineReserve
from utils.database_initializer import DatabaseInitializer
from utils.env_variable_loader import EnvVariableLoader

# Load environment variables
config_loader = EnvVariableLoader()
db_config = config_loader.get_database_config()

# Initialize the DatabaseInitializer using environment variables
db_initializer = DatabaseInitializer(
    db_user=db_config['db_user'],
    db_password=db_config['db_password'],
    db_host=db_config['db_host'],
    db_name=db_config['db_name']
)

def get_reservation(event):

    engine = db_initializer.get_engine_with_db()
    Session = sessionmaker(bind=engine)
    session = Session()

    query_params = event.get('queryStringParameters', {})
    name = query_params.get('name')
    phone_number = query_params.get('phone_number')
    line_id = query_params.get('line_id')

    try:
        reserves = session.query(LineReserve).filter_by(name=name, phone_number=phone_number, line_id=line_id).all()

        if not reserves:
            return None
        
        result = [reserve.as_dict() for reserve in reserves]

        return {
            'statusCode': 200,
            'body': json.dumps(result, ensure_ascii=False)
        }

    except Exception as e:
        print(f"Error fetching reservations: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps({'message': 'Internal server error'})
        }

    finally:
        session.close()


def get_latest_reservation_id():
    try:

        engine = db_initializer.get_engine_with_db()
        Session = sessionmaker(bind=engine)
        session = Session()
        latest_id = session.query(func.max(LineReserve.reservation_id)).scalar()
        session.close()

        return {
            'statusCode': 200,
            'body': json.dumps({'latest_reserve_id': latest_id})
        }

    except ProgrammingError as e:
        print(f"Error fetching latest_reserve_id (likely missing table): {e}")
        return {
            'statusCode': 200,
            'body': json.dumps({'latest_reserve_id': 0})
        }

    except Exception as e:
        print(f"Error fetching latest_reserve_id: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps('Internal server error')
        }
