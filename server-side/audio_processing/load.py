import wave
import numpy as np


#פונקציה שקוראת קובץ שמע ומחזירה את המידע עליו שיעזור להמשך ניתוח נתונים
def load_wav_file(file_path):
    with wave.open(file_path, 'rb') as wav_file:
        #בדיקת קצב הדגימה של השמע
        sample_rate = wav_file.getframerate()
        #בדיקת מספר המסגרות שמע שבקובץ
        n_frames = wav_file.getnframes()
        #קריאת הקובץ כבינארי
        audio = wav_file.readframes(n_frames)
        #הופכים את המידע הבינארי למערך מספרים שלמים
        #כל מספר מייצג את גובה הצליל בנקודת זמן מסויימת
        audio_data = np.frombuffer(audio, dtype=np.int16)

    print(f"[load_wav_file] sample_rate: {sample_rate}, frames: {n_frames}, audio_data shape: {audio_data.shape}")

    return sample_rate, audio_data