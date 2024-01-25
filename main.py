import os
from transcribe import TranscribeAudio
from models.gpt3 import chatgptHandler
from dotenv import load_dotenv
from pytube import YouTube

load_dotenv()

URL = "https://www.youtube.com/watch?v=9otjobweWxI"
yt = YouTube(URL)
video = yt.streams.get_highest_resolution()
videoPath = video.download()
videoPath = os.path.basename(videoPath)

try:
    transcribedAudio = TranscribeAudio("tiny", f"./{videoPath}")
    config = {
        "model":"gpt-3.5-turbo",
        "token": os.getenv("API_KEY"),
        "outputLaguage":"portugues"
    }
    handler = chatgptHandler(config, transcribedAudio.transcription_result)
    handler.sendMessage()
    print(handler.summary)

except Exception as e:
    print(e)
    