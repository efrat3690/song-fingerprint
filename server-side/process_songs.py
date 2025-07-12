import os
from audio_processing.convert import convert_to_wav
from audio_processing.load import load_wav_file
from audio_processing.fft import apply_fft_to_windows
from audio_processing.windows import split_to_windows
from audio_processing.dominant import detect_peaks
from audio_processing.fingerprint_generator import generate_hash
from database.insert import insert_song_to_db, insert_fingerprints_to_db

BASE_URL= r"C:\Users\שרת\Desktop\music"
# פונקציה המנהלת את הכנסת הנתונים לדטה בייס
def process_directory(song_name):
    file_path = f"{BASE_URL}\\{song_name}"
    print(file_path)
    if song_name.lower().endswith(".wav"):
        wav_path = file_path
        #המרת הקובץ- אם הוא לא WAV
    else:
        wav_path = convert_to_wav(file_path)

        #בעיבוד מתבצע רק במקרה וישנה קובץ תקין בפורמט הנדרש
    if wav_path:
        print(" שיר נמצא - מתחילים עיבוד:", song_name)
            # המרה מאות שמע אנלוגי לאות שמע דיגיטלי
        sample_rate, audio_data = load_wav_file(wav_path)
        if sample_rate != 44100:
            print(f" שים לב: קצב הדגימה אינו 44,100 Hz אלא {sample_rate} Hz.")
        else:
            print(f" קצב הדגימה תקין: {sample_rate} Hz.")
        #חיתוך השמע לחלונות זמן
        windows = split_to_windows(audio_data)

            #ביצוע FFT- ניתוח התדרים, עוצמתם, והפאזה שלהם בעבור חלונות הזמן
        spectrogram = apply_fft_to_windows(windows)

            #מציאת התדרים המשמעותיים בכל חלון- אחד מכל תחום
        dominant_freq_matrix = detect_peaks(spectrogram)

            #יצירת טביעת אצבע לשיר- עבור כל חלון
        fingerprints = generate_hash(dominant_freq_matrix)
        print(" טביעות אצבע נוצרו:", len(fingerprints))

            #הכנסת השיר המקורי למסד הנתונים
        song_id = insert_song_to_db(song_name, file_path, len(fingerprints))
        print(" שמירת שיר למסד נתונים")

           # הכנסת טביעות האצבע של השיר למסד הנתונים עם קישוריות לשיר עצמו
        insert_fingerprints_to_db(fingerprints, song_id)
        print(" שמירת טביעות אצבע למסד נתונים")

        if wav_path != file_path:
            os.remove(wav_path)
        print(" סיום עיבוד:", song_name)
        return song_id
