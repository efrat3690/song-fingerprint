from pydub import AudioSegment
import tempfile
import subprocess


def convert_to_wav(file_path):
    try:
        audio = AudioSegment.from_file(file_path)
        audio = audio.set_frame_rate(44100).set_channels(1)  # הדגשה על מונו

        temp_wav = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
        temp_wav.close()  # סגירת הקובץ לפני הכתיבה

        audio.export(temp_wav.name, format="wav")
        print(f"המרה הצליחה, קובץ WAV בנתיב: {temp_wav.name}")
        return temp_wav.name

    except Exception as e:
        print(f" נכשל להמיר את {file_path}: {e}")
        return None


def convert_webm_to_wav(input_path: str, output_path: str):
    subprocess.run([
        "ffmpeg",
        "-y",  # דריסה אוטומטית של הקובץ אם כבר קיים
        "-i", input_path,  # הקלט: קובץ webm
        "-ar", "44100",  # ar = Audio Rate = קצב דגימה (44.1kHz, סטנדרטי)
        "-ac", "1",  # ac = Audio Channels = מונו (ערוץ אחד)
        "-f", "wav",  # פורמט הפלט יהיה wav
        output_path  # הנתיב של קובץ הפלט
    ], check=True)



