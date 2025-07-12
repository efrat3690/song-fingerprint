import numpy as np
from scipy import signal


def preprocess_audio(samples, sample_rate=44100):
    """
    מעבדת את הדגימה הגולמית לפני תחילת התהליך:
    1. מנרמלת את הדגימה לתחום [-1, 1].
    2. מסירה DC offset (מרכזת את הדגימה סביב 0).
    3. מפעילה lowpass filter להסרת רעשים בתדרים גבוהים.

    פרמטרים:
    ----------
    samples : np.ndarray
        הדגימה הגולמית.
    sample_rate : int
        קצב הדגימה (ברירת מחדל: 22,050 Hz).

    פלט:
    ----
    np.ndarray
        הדגימה לאחר עיבוד מוקדם.
    """
    # 1. נרמול הדגימה
    samples = samples / np.max(np.abs(samples))

    # 2. סילוק DC offset
    samples = samples - np.mean(samples)

    # 3. סינון lowpass (כדי להסיר רעש בתדרים גבוהים מ-11kHz)
    nyquist = sample_rate / 2
    cutoff = min(11025, nyquist * 0.95)  # מונע aliasing
    b, a = signal.butter(5, cutoff / nyquist, btype='low')
    samples = signal.filtfilt(b, a, samples)

    return samples
