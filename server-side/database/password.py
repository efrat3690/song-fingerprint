import bcrypt

# הסיסמה שרוצים להצפין
plain_password = "1234"

# הצפנת הסיסמה (הפלט הוא bytes, נמיר אותו ל-string)
hashed_password_bytes = bcrypt.hashpw(plain_password.encode('utf-8'), bcrypt.gensalt())
hashed_password_string = hashed_password_bytes.decode('utf-8')

print(f"הסיסמה הרגילה: {plain_password}")
print(f"הסיסמה המוצפנת (hash): {hashed_password_string}")

# דוגמה לאימות:
# is_correct = bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password_bytes)
# print(f"הסיסמה נכונה? {is_correct}")