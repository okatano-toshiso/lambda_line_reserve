validation_rules = {
    "line_reserves": {
        "required_fields": [
            "reservation_date",
            "count_of_person",
            "name",
            "phone_number",
        ],
        "integer_fields": {
            "fields": ["count_of_person", "reservation_id"],
            "max_values": {"count_of_person": 10},
        },
        "string_fields": {
            "fields": ["name", "room_type"],
            "max_lengths": {"name": 20, "room_type": 50},
        },
        "date_fields": ["reservation_date", "check_in", "check_out"],
        "datetime_fields": ["created_at", "updated_at"],
        "phone_number_fields": ["phone_number"],
    },
    "line_users": {
        "required_fields": ["name", "phone_number"],
        "integer_fields": {"fields": ["age"], "max_values": {"age": 100}},
        "string_fields": {"fields": ["name"], "max_lengths": {"name": 20}},
        "katakana_fields": ["name_kana"],
        "phone_number_fields": ["phone_number"],
        "datetime_fields": ["created_at", "updated_at"],
    },
}
