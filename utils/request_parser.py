import json


class RequestParser:
    def parse_request_body(self, event):
        try:
            return json.loads(event["body"])
        except (json.JSONDecodeError, KeyError) as e:
            raise ValueError("Invalid request body") from e
