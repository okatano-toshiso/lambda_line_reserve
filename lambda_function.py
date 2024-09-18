from reserve_confirm import get_max_reservation_id, get_reservation
import reserve_regist
import reserve_confirm
import reserve_update
import reserve_cancel

def lambda_handler(event, context):
    method = event['httpMethod']
    query_params = event.get('queryStringParameters', {})

    if method == 'POST':
        return reserve_regist.handler(event, context)
    elif method == 'GET':
        if query_params.get('type') == 'max_id':
            return get_max_reservation_id()
        else:
            return get_reservation()
    elif method == 'PUT':
        return reserve_update.handler(event, context)
    elif method == 'DELETE':
        return reserve_cancel.handler(event, context)
    else:
        return {
            'statusCode': 405,
            'body': 'Method Not Allowed'
        }
