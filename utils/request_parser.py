import json

class RequestParser:
    def parse_request_body(self, event):
        """
        リクエストイベントからJSONボディを取得し、辞書に変換します。
        :param event: Lambdaイベントオブジェクト
        :return: JSONデータの辞書
        """
        try:
            request_body = json.loads(event['body'])
            return request_body
        except (json.JSONDecodeError, KeyError) as e:
            print(f"無効なリクエストボディ: {e}")
            raise ValueError('Invalid request body') from e
