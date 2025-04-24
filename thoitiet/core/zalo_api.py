import requests
from rest_framework.exceptions import APIException

ZALO_OPEN_API_URL = "https://graph.zalo.me/v2.0/me/info"
ZALO_FOLLOWERS_URL = "https://openapi.zalo.me/v2.0/oa/getfollowers"
ZALO_PERMISSION_URL = "https://openapi.zalo.me/v2.0/app/location/permission-request"
ZALO_TOKEN_URL = "https://openapi.zalo.me/v2.0/app/location/token"
ZALO_LOCATION_URL = "https://openapi.zalo.me/v2.0/app/location"
ZALO_ERROR_URL = "https://openapi.zalo.me/v2.0/app/location/error"
ZALO_SECRET_KEY = "your_zalo_app_secret_key"  # Thay bằng secret key của bạn

def get_user_location(access_token: str, token: str) -> dict:
    headers = {
        "access_token": access_token,
        "code": token,
        "secret_key": ZALO_SECRET_KEY
    }
    response = requests.get(ZALO_OPEN_API_URL, headers=headers)
    if response.status_code != 200:
        raise APIException(detail=f"Zalo API error: {response.json()}", code=400)
    data = response.json()
    if data.get("error") != 0:
        raise APIException(detail=data.get("message"), code=400)
    return data.get("data", {})

def check_oa_follow_status(access_token: str, user_id: str) -> dict:
    params = {"access_token": access_token, "user_id": user_id}
    response = requests.get(ZALO_FOLLOWERS_URL, params=params)
    if response.status_code != 200:
        raise APIException(detail=f"Zalo API error: {response.json()}", code=400)
    data = response.json()
    if data.get("error") != 0:
        raise APIException(detail=data.get("message"), code=400)
    return data.get("data", {})

def request_location_permission(access_token: str, user_id: str) -> dict:
    params = {"access_token": access_token, "user_id": user_id}
    response = requests.get(ZALO_PERMISSION_URL, params=params)
    if response.status_code != 200:
        raise APIException(detail=f"Zalo API error: {response.json()}", code=400)
    return response.json()

def get_location_token(access_token: str, user_id: str) -> dict:
    params = {"access_token": access_token, "user_id": user_id}
    response = requests.get(ZALO_TOKEN_URL, params=params)
    if response.status_code != 200:
        raise APIException(detail=f"Zalo API error: {response.json()}", code=400)
    return response.json()

def get_location_with_token(access_token: str, token: str, user_id: str) -> dict:
    params = {"access_token": access_token, "token": token, "user_id": user_id}
    response = requests.get(ZALO_LOCATION_URL, params=params)
    if response.status_code != 200:
        raise APIException(detail=f"Zalo API error: {response.json()}", code=400)
    return response.json()

def check_location_error(access_token: str, user_id: str) -> dict:
    params = {"access_token": access_token, "user_id": user_id}
    response = requests.get(ZALO_ERROR_URL, params=params)
    if response.status_code != 200:
        raise APIException(detail=f"Zalo API error: {response.json()}", code=400)
    return response.json()