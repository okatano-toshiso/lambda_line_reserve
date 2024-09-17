import reserve_regist
import reserve_confirm
import reserve_update
import reserve_cancel

def lambda_handler(event, context):
    method = event['httpMethod']

    if method == 'POST':
        return reserve_regist.handler(event, context)
    elif method == 'GET':
        return reserve_confirm.handler(event, context)
    elif method == 'PUT':
        return reserve_update.handler(event, context)
    elif method == 'DELETE':
        return reserve_cancel.handler(event, context)
    else:
        return {
            'statusCode': 405,
            'body': 'Method Not Allowed'
        }
