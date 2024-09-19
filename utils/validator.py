from datetime import datetime
import re
from utils.validation_rules import validation_rules

class Validator:
    @staticmethod
    def validate_required_fields(data, *required_fields):
        for field in required_fields:
            if field not in data or not data[field]:
                raise ValueError(f"Missing or empty required field: {field}")

    @staticmethod
    def validate_integer(data, *field_names, max_value=None):
        for field_name in field_names:
            value = data.get(field_name)
            if value is not None:  # 値が存在する場合のみチェック
                if not isinstance(value, int):
                    raise ValueError(f"Field '{field_name}' must be an integer")
                if max_value is not None and value > max_value:
                    raise ValueError(f"Field '{field_name}' must not be greater than {max_value}")

    @staticmethod
    def validate_date_format(data, *field_names, date_format='%Y-%m-%d'):
        for field_name in field_names:
            date_str = data.get(field_name)
            try:
                datetime.strptime(date_str, date_format)
            except ValueError:
                raise ValueError(f"Invalid date format for '{field_name}', should be {date_format}")

    @staticmethod
    def validate_datetime_format(data, *field_names, datetime_format='%Y-%m-%d %H:%M:%S'):
        for field_name in field_names:
            datetime_str = data.get(field_name)
            if isinstance(datetime_str, datetime):
                datetime_str = datetime_str.strftime(datetime_format)
            elif datetime_str:
                datetime_str = datetime_str.strip()
            try:
                datetime.strptime(datetime_str, datetime_format)
            except ValueError:
                raise ValueError(f"Invalid datetime format for '{field_name}', should be {datetime_format}")

    @staticmethod
    def validate_string(data, *field_names, max_length=None):
        for field_name in field_names:
            value = data.get(field_name)
            if not isinstance(value, str):
                raise ValueError(f"Field '{field_name}' must be a string")
            if max_length and len(value) > max_length:
                raise ValueError(f"Field '{field_name}' exceeds maximum length of {max_length}")

    @staticmethod
    def validate_phone_number(data, *field_names, min_length=10, max_length=11):
        phone_number_pattern = re.compile(r'^\d+$')
        for field_name in field_names:
            phone_number = data.get(field_name)
            if not phone_number_pattern.match(phone_number):
                raise ValueError(f"Field '{field_name}' must contain only digits")
            if not (min_length <= len(phone_number) <= max_length):
                raise ValueError(f"Field '{field_name}' must be between {min_length} and {max_length} digits")

    @staticmethod
    def validate_katakana(data, *field_names):
        katakana_pattern = re.compile(r'^[\u30A0-\u30FF\u30FC]+$')
        for field_name in field_names:
            value = data.get(field_name)
            print(f"Validating field '{field_name}': {value}")
            if not value:
                raise ValueError(f"Field '{field_name}' must not be empty or None")
            if not isinstance(value, str):
                raise ValueError(f"Field '{field_name}' must be a string")
            if not katakana_pattern.fullmatch(value):
                raise ValueError(f"Field '{field_name}' must contain only Katakana characters")

    @staticmethod
    def validate_data(data, data_type):
        rules = validation_rules.get(data_type)
        if not rules:
            raise ValueError(f"No validation rules defined for data type '{data_type}'")
        Validator.validate_required_fields(data, *rules['required_fields'])
        for field_name in rules['integer_fields']['fields']:
            max_value = rules['integer_fields']['max_values'].get(field_name)
            Validator.validate_integer(data, field_name, max_value=max_value)
        for field_name in rules['string_fields']['fields']:
            max_length = rules['string_fields']['max_lengths'].get(field_name)
            Validator.validate_string(data, field_name, max_length=max_length)
        if 'date_fields' in rules:
            Validator.validate_date_format(data, *rules['date_fields'])
        if 'phone_number_fields' in rules:
            Validator.validate_phone_number(data, *rules['phone_number_fields'])
        if 'datetime_fields' in rules:
            Validator.validate_datetime_format(data, *rules['datetime_fields'])
        if 'katakana_fields' in rules:
            Validator.validate_katakana(data, *rules['katakana_fields'])
