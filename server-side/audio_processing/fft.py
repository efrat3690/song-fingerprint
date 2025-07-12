import numpy as np

# חישוב FFT על כל חלון עם Zero padding
def apply_fft_to_windows(windows):
    spectrogram = []
    for window in windows:
        fft_result = np.fft.rfft(window, n=len(window) * 2)  # Zero padding
        spectrogram.append(fft_result)
    return spectrogram