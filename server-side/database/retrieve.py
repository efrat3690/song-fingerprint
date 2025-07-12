import os
from database.find import get_song_by_id

BASE_URL = "http://127.0.0.1:8000/static"

def get_song_details(ranked_songs):
    """שליפת פרטי שירים והכנת התוצאה להצגה."""
    results = []
    for song_id, score_data in ranked_songs:
        song_data = get_song_by_id(song_id)  # שליפה ממסד הנתונים
        if song_data:
            song_data.pop('_id', None)  # אין צורך ב-ID פנימי
            song_data['score'] = round(score_data["score"], 2)
            file_name = song_data.get("song_name", "")
            song_data["file_path"] = f"{BASE_URL}/{file_name}"
            display_name, _ = os.path.splitext(file_name)
            song_data["song_name"] = display_name
            results.append(song_data)
        else:
            print(f"[DEBUG] ✖ שיר לא נמצא במסד הנתונים: {song_id}")

    return results
