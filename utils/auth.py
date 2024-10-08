import json


def get_access_token_from_header(headers):
    """
    Authorizationヘッダーからアクセストークンを取得する共通メソッド
    :param headers: リクエストヘッダー（辞書形式）
    :return: アクセストークン（文字列）またはエラーレスポンス
    """
    auth_header = headers.get("Authorization", "")

    # Authorizationヘッダーが存在しない場合
    if not auth_header:
        return {
            "statusCode": 401,
            "body": json.dumps("Authorization header missing"),
        }, None

    # 'Bearer {token}'形式であることを確認し、トークンを取得
    try:
        token_type, access_token = auth_header.split(" ")
        if token_type.lower() != "bearer":
            return {
                "statusCode": 401,
                "body": json.dumps("Invalid token type. Expected Bearer."),
            }, None
        return None, access_token
    except ValueError:
        return {
            "statusCode": 400,
            "body": json.dumps("Invalid Authorization header format"),
        }, None
