
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


def if_exist(song: dict):
    existing = songs_collection.find_one({"song_name": song["song_name"]})
    return existing is not None


def insert_song_to_db(song_name, file_path, num_finger):
    # יוצרים מסמך עם שם השיר ונתיבו בשרת
    song_doc = {
        "song_name": song_name,
        "file_path": file_path,
        "num_finger": num_finger
    }
    # שומרים את המסמך במסד הנתונים ומחזירים את המזהה הייחודי
    result = songs_collection.insert_one(song_doc)
    return result.inserted_id


def insert_fingerprints_to_db(fingerprints, song_id):
    fingerprint_docs = []
    # בונים רשימת מסמכים – כל אחד מייצג hash של עוגן-יעד, עם הקיזוז וזיהוי השיר
    for hash_val, offset in fingerprints:
        doc = {
            "hash": hash_val,
            "offset": offset,
            "song_id": song_id
        }
        fingerprint_docs.append(doc)
    # מוסיפים את כל הטביעות למסד הנתונים במכה אחת
    if fingerprint_docs:
        fingerprints_collection.insert_many(fingerprint_docs)
