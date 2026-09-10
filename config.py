# config.py
STORAGE_MODE = "local"

AWS_CONFIG = {
    "access_key": "YOUR_AWS_ACCESS_KEY",
    "secret_key": "YOUR_AWS_SECRET_KEY",
    "region": "ap-south-1",
    "bucket_name": "iot-secure-search-bucket"
}

USERS = {
    "owner":  {"role": "admin",   "can_upload": True,  "can_search": True, "allowed_keywords": "*"},
    "user1":  {"role": "premium", "can_upload": False, "can_search": True, "allowed_keywords": "*"},
    "user2":  {"role": "basic",   "can_upload": False, "can_search": True, "allowed_keywords": ["camera", "door_lock", "front_door"]},
    "user3":  {"role": "guest",   "can_upload": False, "can_search": True, "allowed_keywords": ["camera"]},
}

RANKING_WEIGHTS = {
    "exact_match": 10,
    "partial_match": 5,
    "recency": 3,
    "owner_priority": 2,
}

# Alert settings
ALERTS = {
    "unauthorized_access": True,
    "restricted_keyword": True,
    "multiple_failed_attempts": 3,       # alert after 3 attempts
    "log_file": "audit/alerts.log"
}