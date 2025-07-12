# from collections import defaultdict, Counter
# from itertools import count
#
#
# #  מחשבת את הפרשי הזמנים (delta) בין ההקלטה לשירים במסד
# def analyze_matches(matches):
#     song_diffs = defaultdict(Counter)
#     monee = 0
#     for i, match in enumerate(matches):
#         song_id = match["song_id"]  # מזהה השיר במסד
#         time_song = match["db_offset"]  # הזמן בו הופיעה טביעת האצבע בשיר
#         time_rec = match["recording_offset"]  # הזמן בו הופיעה טביעת האצבע בהקלטה
#         if time_song is None or time_rec is None:
#             continue  # מדלגים על התאמות חסרות
#         delta = time_song - time_rec  # הפרש הזמן בין ההקלטה לשיר
#         song_diffs[song_id][delta] += 1
#         monee+=1
#     print(f"[DEBUG] סך שירים שנותחו: {len(song_diffs)}")
#     print(monee)
#     return song_diffs  # מחזיר את מילון הפרשי הזמנים לכל שיר
# # from collections import defaultdict, Counter
# #
# # def analyze_matches(
# #     matches
# # ):
# #     song_diffs = defaultdict(Counter)  # song_id -> Counter של delta -> count
# #
# #     for match in matches:
# #         song_id = match['song_id']
# #         delta = match['db_offset'] - match['recording_offset']
# #         song_diffs[song_id][delta] += 1
# #
# #     print(f"[DEBUG] סך שירים שנותחו: {len(song_diffs)}")
# #     return song_diffs
