from pymongo import MongoClient
from bson import ObjectId, SON
from collections import defaultdict, Counter
import time
from typing import List, Tuple


client = MongoClient("mongodb://localhost:27017/")
db = client["AcousticFingerprint"]
fingerprints_collection = db["fingerprints"]
songs_collection = db["songs"]
admin_collection = db["admin"]


def admin_connect(data):
    return admin_collection.find_one({"username": data.username})


def all_song():
    # אם הצליח – נביא את כל השירים

    songs = list(songs_collection.find())
    for song in songs:
        song["id"] = str(song["_id"])
        del song["_id"]  # מסיר את השדה הבעייתי
    return songs



def get_song_by_id(song_id):
    return songs_collection.find_one({"_id": ObjectId(song_id)})


def find_and_analyze_matches(query_fingerprints,
                             batch_size=100,
                             time_tolerance=0.1,
                             min_matches_threshold=5):
    #מחפש את טביעת האצבע בדאטאבייס ומבצע ניתוח עקביות זמן באותה פעולה
    song_analysis = defaultdict(list)

    hash_values = [fp[0] for fp in query_fingerprints]
    hash_to_query_offset = {fp[0]: fp[1] for fp in query_fingerprints}

    for i in range(0, len(hash_values), batch_size):
        batch_hashes = hash_values[i:i + batch_size]
        cursor = fingerprints_collection.find(
            {"hash": {"$in": batch_hashes}},
            {"hash": 1, "offset": 1, "song_id": 1, "_id": 0}
        )

        for match in cursor:
            query_offset = hash_to_query_offset.get(match["hash"])
            if query_offset is not None:
                time_diff = match["offset"] - query_offset
                song_analysis[match["song_id"]].append(time_diff)

    song_scores = {}
    for song_id, time_diffs in song_analysis.items():
        if len(time_diffs) < min_matches_threshold:
            continue
        rounded_diff = [round(td, 1) for td in time_diffs]
        diff_counter = Counter(rounded_diff)
        most_common_diff, _count = diff_counter.most_common(1)[0]

        consistent_matches = sum(
            1 for td in time_diffs if abs(td - most_common_diff) <= time_tolerance
        )
        #חישוב היחס בין ההתאמות החזקות לכלל ההתאמות
        consistency_ratio = consistent_matches / len(time_diffs)
        score = min(consistent_matches * consistency_ratio, 100)

        song_scores[song_id] = {
            "score": score,
            "total_matches": len(time_diffs),
            "consistent_matches": consistent_matches,
            "consistency_ratio": consistency_ratio,
            "time_offset": most_common_diff,
            "confidence": min(score / 20, 1.0)
        }

    return song_scores
