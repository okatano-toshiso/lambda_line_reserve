def handler(event, context):
    # 予約キャンセルのロジック
    return {
        'statusCode': 200,
        'body': '予約が正常にキャンセルされました。'
    }
