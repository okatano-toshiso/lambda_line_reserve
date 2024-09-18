import json
from sqlalchemy import func
from sqlalchemy.orm import sessionmaker
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
def get_reservation():
    return {
        'statusCode': 200,
        'body': '予約を確認してください。'
    }


def get_max_reservation_id():
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
    except Exception as e:
        print(f"Error fetching latest_reserve_id: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps('Internal server error')
        }
