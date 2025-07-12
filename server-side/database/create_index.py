# create_index.py

from pymongo import MongoClient


# התחברות למסד הנתונים
client = MongoClient("mongodb://localhost:27017/")
db = client["AcousticFingerprint"]
fingerprints_collection = db["fingerprints"]

# יצירת אינדקס על השדה 'hash' (אם קיים כבר, לא ייווצר שוב)
result = fingerprints_collection.create_index("hash")
print(f"אינדקס נוצר או כבר קיים: {result}")
