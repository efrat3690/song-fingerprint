import numpy as np
from audio_processing.initial_cleaning import preprocess_audio


def split_to_windows(samples, window_size=2048, hop_size=512, sample_rate=44100):
    """חיתוך לחלונות עם חפיפה והכפלה ב־Hann"""
    samples = preprocess_audio(samples, sample_rate)

    windows = []
    hann_window = np.hanning(window_size)

    for start in range(0, len(samples) - window_size + 1, hop_size):
        window = samples[start:start + window_size]
        windows.append(window * hann_window)

    print(f"[split_to_windows] Created {len(windows)} windows, each of size {window_size}")
    return windows