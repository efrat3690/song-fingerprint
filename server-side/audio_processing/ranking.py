#
# # מדרגת את ההתאמות החזקות לפי מספר ההתאמות (count) מהגבוה לנמוך
# def rank_matches(strong_matches):
#     # ממיינת את ההתאמות לפי השדה 'count' – מספר הפעמים שהפרש הזמן הופיע
#     ranked = sorted(strong_matches, key=lambda match: match['count'], reverse=True)
#     print("[DEBUG] דירוג התאמות:")
#     for match in ranked:
#         # מדפיסה כל התאמה מדורגת: מזהה שיר, כמות ההתאמות והפרש הזמן
#         print(f"  שיר: {match['song_id']}, ספירה: {match['count']}, אופסט: {match['best_offset']}")
#     return ranked  # מחזירה את רשימת ההתאמות המדורגת
