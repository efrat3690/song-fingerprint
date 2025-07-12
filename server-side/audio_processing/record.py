from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from datetime import datetime, timedelta
import bcrypt
from identify import identify_song_from_bytes
from audio_processing.convert  import convert_to_wav, convert_webm_to_wav
from database.find import admin_connect, all_song
from database.insert import if_exist
from database.update_and_dalate import update_song_in_db, delete_song_in_db
from process_songs import process_directory
import tempfile
import subprocess
from bson import ObjectId
import os
from dotenv import load_dotenv


router = APIRouter()


load_dotenv()  # טוען את הקובץ .env
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/admin/token")


# הצפנת סיסמה
def verify_password(plain_password, hashed_password):
    return bcrypt.checkpw(plain_password.encode(), hashed_password.encode())


# יצירת טוקן
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=30))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


# אימות טוקן לכל בקשה שמצריכה הרשאה
def get_current_admin(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="בעיה באימות")
        return username
    except JWTError:
        raise HTTPException(status_code=401, detail="טוקן לא תקף")


# התחברות – מסלול חדש
@router.post("/admin/token")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    admin = admin_connect(form_data)
    if not admin:
        raise HTTPException(status_code=401, detail="שם משתמש שגוי")
    if not verify_password(form_data.password, admin["password"]):
        raise HTTPException(status_code=401, detail="סיסמה שגויה")
    access_token = create_access_token(data={"sub": form_data.username})
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/admin/add_song_file")
async def add_song_file(file: UploadFile = File(...), song_name: str = Form(...)):
    if not song_name or not file:
        raise HTTPException(status_code=400, detail="יש למלא את כל השדות")

    # בדיקה אם קיים כבר במסד
    if if_exist({"song_name": song_name}):
        raise HTTPException(status_code=400, detail="שיר זה כבר קיים")

    # שמירה זמנית של הקובץ
    temp_dir = "temp_uploads"
    os.makedirs(temp_dir, exist_ok=True)
    temp_path = os.path.join(temp_dir, file.filename)

    with open(temp_path, "wb") as f:
        f.write(await file.read())

    try:
        result = process_directory(file.filename)
        return {
            "success": True,
            "message": f"שיר נוסף בהצלחה עם מזהה: {result}"
        }
    except Exception as e:
        return {
            "success": False,
            "message": f"שגיאה: {str(e)}"
        }
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)



@router.put("/admin/update_songs/{song_id}")
async def update_song(song_id: str, song_data: dict, current_admin: str = Depends(get_current_admin)):
    if not ObjectId.is_valid(song_id):
        raise HTTPException(status_code=400, detail="Invalid song ID")

    result = update_song_in_db(song_id, song_data)

    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Song not found")

    if result.modified_count == 0:
        return {"message": "No changes made"}

    return {"message": "Song updated successfully"}


@router.delete("/admin/delete_songs/{song_id}")
async def delete_song(song_id: str, current_admin: str = Depends(get_current_admin)):
    if not ObjectId.is_valid(song_id):
        raise HTTPException(status_code=400, detail="Invalid song ID")

    success = delete_song_in_db(song_id)

    if not success:
        raise HTTPException(status_code=404, detail="Song not found")

    return {"message": "Song deleted successfully"}


# קבלת שירים – רק אם המשתמש מחובר
@router.get("/admin/songs")
def get_songs(current_admin: str = Depends(get_current_admin)):
    result = all_song()
    return JSONResponse(status_code=200, content={"success": True, "songs": result})


@router.post("/upload-audio/")
async def upload_audio(file: UploadFile = File(...)):
    print("התקבלה בקשה עם קובץ:", file.filename)

    contents = await file.read()
    file_ext = file.filename.split('.')[-1].lower()
    mime_type = file.content_type
    print("סוג הקובץ:", mime_type, "| סיומת:", file_ext)

    tmp_input_path = ""
    tmp_output_path = ""

    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=f".{file_ext}") as tmp_input:
            tmp_input.write(contents)
            tmp_input_path = tmp_input.name

        if mime_type == "audio/webm" or file_ext == "webm":
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_output:
                tmp_output_path = tmp_output.name
            convert_webm_to_wav(tmp_input_path, tmp_output_path)
            wav_path = tmp_output_path

        elif file_ext == "wav":
            wav_path = tmp_input_path

        else:
            print("ממיר את הקובץ מMP3 לWAV")
            wav_path = convert_to_wav(tmp_input_path)

        result = identify_song_from_bytes(wav_path)
        print("תוצאה מהזיהוי:", result)

        if isinstance(result, dict) and "error" in result:
            return JSONResponse(status_code=400, content={"success": False, "error": result["error"]})

        return JSONResponse(status_code=200, content={"success": True, "songs": result})

    except subprocess.CalledProcessError:
        return JSONResponse(status_code=500, content={"success": False, "error": "שגיאה בהמרת הקלטה ל-WAV"})

    except Exception as e:
        return JSONResponse(status_code=500, content={"success": False, "error": str(e)})

    finally:
        for path in [tmp_input_path, tmp_output_path]:
            if path and os.path.exists(path):
                os.remove(path)


@router.get("/routes")
def list_routes():
    return [route.path for route in router.routes]