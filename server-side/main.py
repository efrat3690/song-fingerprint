from fastapi import FastAPI
from audio_processing.record import router
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from process_songs import process_directory

# #בנית שרת המאזין לבקשות לקוח
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
print("✅ CORS middleware loaded")
app.include_router(router)
app.mount("/static", StaticFiles(directory="C:/Users/שרת/Desktop/music"), name="static")


