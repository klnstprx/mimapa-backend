from datetime import datetime, timedelta
from jose import jwt
import os
import requests
import cloudinary.uploader

# JWT configuration
SECRET_KEY = os.getenv("SECRET_KEY", "your_default_secret_key")
ALGORITHM = "HS256"


def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.now() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def geocode_address(address: str):
    GEOCODING_API_KEY = os.getenv("GEOCODING_API_KEY")
    url = "https://api.opencagedata.com/geocode/v1/json"
    params = {
        "q": address,
        "key": GEOCODING_API_KEY,
    }
    response = requests.get(url, params=params)
    if response.status_code != 200:
        raise Exception("Geocoding API request failed")
    data = response.json()
    if len(data["results"]) == 0:
        raise Exception("Address not found")
    geometry = data["results"][0]["geometry"]
    return geometry["lat"], geometry["lng"]


def upload_image_to_cloudinary(file):
    cloudinary.config(
        cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
        api_key=os.getenv("CLOUDINARY_API_KEY"),
        api_secret=os.getenv("CLOUDINARY_API_SECRET"),
    )
    result = cloudinary.uploader.upload(file.file)
    return result["secure_url"]
