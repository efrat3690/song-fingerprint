import numpy as np
from scipy.signal import find_peaks
import time


# מחפש את הפיקים החזקים ביותר בכל חלון
def detect_peaks(spectrogram, amp_min=40, max_peaks_per_frame=3, verbose=True):
    start_time = time.time()
    peaks = []

    for t, spec in enumerate(spectrogram):
        amp_spec = np.abs(spec)
        strong_peaks, properties = find_peaks(amp_spec, height=amp_min)

        if len(strong_peaks) > max_peaks_per_frame:
            heights = properties["peak_heights"]
            sorted_indices = np.argsort(heights)[::-1]
            top_peaks = strong_peaks[sorted_indices[:max_peaks_per_frame]]
        else:
            top_peaks = strong_peaks

        for p in top_peaks:
            peaks.append((t, p))

    # דיבוג
    elapsed = time.time() - start_time
    if verbose:
        print(f"\n detect_peaks סיים | זמן ריצה: {elapsed:.2f} שניות")
        print(f" מספר הפיקים הכולל: {len(peaks)}")

    return peaks
