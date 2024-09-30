from reserve_confirm import get_latest_reservation_id, get_reservation
import reserve_regist
import reserve_update
import reserve_cancel
from utils.models import Base
from utils.env_variable_loader import EnvVariableLoader
from utils.database_initializer import DatabaseInitializer

# Initialize the Database once (outside of the handler if appropriate to reuse connections)
config_loader = EnvVariableLoader()
db_config = config_loader.get_database_config()
db_initializer = DatabaseInitializer(
    db_user=db_config['db_user'],
    db_password=db_config['db_password'],
    db_host=db_config['db_host'],
    db_name=db_config['db_name']
)


def lambda_handler(event, context):

    try:
        db_initializer.create_database_if_not_exists()
        print("Database created or already exists.")
    except Exception as e:
        print(f"Failed to create database: {e}")
    
    try:
        db_initializer.create_tables(Base)
        print("Tables created or already exist.")
    except Exception as e:
        print(f"Failed to create tables: {e}")

    method = event['httpMethod']
    query_params = event.get('queryStringParameters', {})

    if method == 'POST':
        return reserve_regist.handler(event, context, db_initializer)
    elif method == 'GET':
        if query_params.get('type') == 'latest_id':
            return get_latest_reservation_id(db_initializer)
        else:
            return get_reservation(event, db_initializer)
    elif method == 'PUT':
        return reserve_update.handler(event, context, db_initializer)
    elif method == 'DELETE':
        return reserve_cancel.handler(event, context, db_initializer)
    else:
        return {
            'statusCode': 405,
            'body': 'Method Not Allowed'
        }
