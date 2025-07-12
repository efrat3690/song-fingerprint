import hashlib
import time


# מחבר פיקים קרובים והופך אותם להאש בצורת (f1, f2, delta_t), כולל הדפסת סטטיסטיקה
def generate_hash(peaks, fan_out=5, verbose=True):
    start_time = time.time()
    hashes = []
    total_pairs = 0
    skipped_pairs = 0

    for i in range(len(peaks)):
        t1, f1 = peaks[i]
        for j in range(1, fan_out + 1):
            if i + j < len(peaks):
                t2, f2 = peaks[i + j]
                delta_t = t2 - t1

                if delta_t == 0:
                    skipped_pairs += 1
                    continue

                raw_string = f"{f1}|{f2}|{delta_t}"
                hash_val = hashlib.md5(raw_string.encode()).hexdigest()[:16]
                hashes.append((hash_val, t1))
                total_pairs += 1

        # דיבוג
    if verbose:
        unique_patterns = set(f"{f1}|{f2}|{t2 - t1}"
                              for i in range(len(peaks))
                              for j in range(1, fan_out + 1)
                              if i + j < len(peaks)
                              for t1, f1 in [peaks[i]]
                              for t2, f2 in [peaks[i + j]]
                              if (t2 - t1) != 0)

        elapsed = time.time() - start_time
        print(f"\n Total peaks received: {len(peaks)}")
        print(f" Total hash pairs created: {total_pairs}")
        print(f" Skipped pairs (delta_t=0): {skipped_pairs}")
        print(f" Unique pattern structures: {len(unique_patterns)}")
        print(f" Total hash entries: {len(hashes)}")
        print(f"Time range in frames: {peaks[-1][0] - peaks[0][0] if peaks else 0}")
        print(f" Avg hashes per second (approx): {round(total_pairs / ((peaks[-1][0] - peaks[0][0]) + 1), 2) if peaks else 0}")
        print(f"⏱ זמן ריצה generate_hash: {elapsed:.2f} שניות")

    return hashes
