#סינון ודירוג התוצאה בהתאם לקריטריונים.

def filter_and_rank_results(song_scores, confidence_threshold=0.3, min_matches_threshold=5):
    filtered = {
        song_id: data for song_id, data in song_scores.items()
        if data["confidence"] >= confidence_threshold
           and data["consistent_matches"] >= min_matches_threshold
    }
    return sorted(filtered.items(), key=lambda x: x[1]["score"], reverse=True)
