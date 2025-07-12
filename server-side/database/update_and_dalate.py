from pymongo import MongoClient
from passlib.context import CryptContext
from fastapi.responses import JSONResponse
from fastapi import Request
from passlib.hash import bcrypt
from bson import ObjectId


# התחברות למסד הנתונים
client = MongoClient("mongodb://localhost:27017/")
db = client["AcousticFingerprint"]
songs_collection = db["songs"]
fingerprints_collection = db["fingerprints"]
users_collection = db["users"]
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def update_song_in_db(song_id: str, update_data: dict):
    return songs_collection.update_one(
        {"_id": ObjectId(song_id)},
        {"$set": {
            "song_name": update_data.get("song_name"),
            "file_path": update_data.get("file_path")
        }}
    )


def delete_song_in_db(song_id: str):
    result = songs_collection.delete_one({"_id": ObjectId(song_id)})
    delete_result = fingerprints_collection.delete_many({"song_id": ObjectId(song_id)})
    if result.deleted_count == 0 or delete_result.deleted_count == 0:
        return False
    return True
