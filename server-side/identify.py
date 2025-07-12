from audio_processing.load import load_wav_file
from audio_processing.windows import split_to_windows
from audio_processing.fft import apply_fft_to_windows
from audio_processing.dominant import detect_peaks
from audio_processing.fingerprint_generator import generate_hash
from database.find import find_and_analyze_matches
from audio_processing.noise_filtering import filter_and_rank_results
from database.retrieve import get_song_details

#    זיהוי שיר מקובץ WAV והדפסות דיבאגר להתאמות, סינונים ודירוג.
def identify_song_from_bytes(wav_path):
    if wav_path:
        # טעינה
        sample_rate, audio_data = load_wav_file(wav_path)
        if sample_rate != 44100:
            print(f"[DEBUG] קצב הדגימה אינו 44,100 Hz אלא {sample_rate} Hz.")
        else:
            print(f" [DEBUG] קצב הדגימה תקין: {sample_rate} Hz.")

        # חיתוך לחלונות
        windows = split_to_windows(audio_data)
        print(f"[DEBUG]  סך חלונות שנוצרו: {len(windows)}")

        # FFT
        spectrogram = apply_fft_to_windows(windows)
        print(f"[DEBUG]  סך חלונות שעברו FFT: {len(spectrogram)}")

        # זיהוי התדרים הדומיננטיים
        dominant_freq_matrix = detect_peaks(spectrogram)
        print(f"[DEBUG]  סך פיקים דומיננטיים: {len(dominant_freq_matrix)}")

        # יצירת טביעות אצבע
        fingerprints = generate_hash(dominant_freq_matrix)
        print(f"[DEBUG]  סך טביעות אצבע שהופקו: {len(fingerprints)}")

        # חיפוש התאמות
        match = find_and_analyze_matches(fingerprints)
        print(f"[DEBUG]  סך התאמות גולמיות מול הדאטאבייס: {len(match)}")

        # סינון להתאמות חזקות
        strong_matches = filter_and_rank_results(match)

        # מיון התוצאה והכנה לשליפה
        ranked_songs = get_song_details(strong_matches)

        for i, song in enumerate(ranked_songs, 1):
            print(f"[DEBUG] {i}. {song.get('song_name')} | ציון: {song.get('score', 'N/A')}")

        return ranked_songs
    else:
        return []
