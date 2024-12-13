from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    UploadFile,
    File,
    Form,
)
from typing import List, Dict
from models import Marker, MarkerCreate, Visit
from database import markers_collection, visits_collection
from auth import get_current_user
from bson.objectid import ObjectId
import asyncio
from utils import geocode_address, upload_image_to_cloudinary
from datetime import datetime

router = APIRouter()


# Get markers for the current user
@router.get("/", response_model=List[Marker])
async def get_markers(user_info: Dict[str, str] = Depends(get_current_user)):
    email = user_info["email"]
    query = {"email": email}
    markers_cursor = markers_collection.find(query)
    markers = []
    async for marker in markers_cursor:
        marker["id"] = str(marker["_id"])
        markers.append(Marker(**marker))
    return markers


# Add a new marker
@router.post("/", response_model=Marker)
async def add_marker(
    lugar: str = Form(...),
    image: UploadFile = File(None),
    user_info: Dict[str, str] = Depends(get_current_user),
):
    current_user = user_info["email"]

    # Geocode address to get lat and lon
    try:
        lat, lon = await asyncio.to_thread(geocode_address, lugar)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    marker_dict = {
        "lugar": lugar,
        "lat": lat,
        "lon": lon,
        "email": current_user,
    }

    # Upload image if provided
    if image is not None:
        try:
            image_url = await asyncio.to_thread(upload_image_to_cloudinary, image)
            marker_dict["imagen"] = image_url
        except Exception as e:
            raise HTTPException(status_code=500, detail="Image upload failed")

    result = await markers_collection.insert_one(marker_dict)
    marker_dict["id"] = str(result.inserted_id)

    return Marker(**marker_dict)


# View another user's map
@router.get("/user/{user_email}", response_model=List[Marker])
async def view_user_markers(
    user_email: str, user_info: Dict[str, str] = Depends(get_current_user)
):
    current_user = user_info["email"]
    token = user_info["token"]
    query = {"email": user_email}
    markers_cursor = markers_collection.find(query)
    markers = []
    async for marker in markers_cursor:
        marker["id"] = str(marker["_id"])
        markers.append(Marker(**marker))

    # Log the visit
    visit = {
        "timestamp": datetime.now(),
        "visited_user_email": user_email,
        "visitor_email": current_user,
        "token": f"Bearer {token}",
    }
    await visits_collection.insert_one(visit)
    return markers


# Get visits for the current user
@router.get("/visits/", response_model=List[Visit])
async def get_visits(user_info: Dict[str, str] = Depends(get_current_user)):
    current_user = user_info["email"]
    query = {"visited_user_email": current_user}
    visits_cursor = visits_collection.find(query).sort("timestamp", -1)
    visits = []
    async for visit in visits_cursor:
        visits.append(Visit(**visit))
    return visits
