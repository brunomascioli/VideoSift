<<<<<<< HEAD
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
    
=======
import os
from transcribe import TranscribeAudio
from models.gpt3 import chatgptHandler
from models.bard import bardHandler
from dotenv import load_dotenv
from pytube import YouTube

load_dotenv()
################## Video Downlaod ##################
URL = "https://www.youtube.com/watch?v=9otjobweWxI"
yt = YouTube(URL)
video = yt.streams.get_highest_resolution()
videoPath = video.download()
videoPath = os.path.basename(videoPath)
################## Tests ##################
modelAI = "bard" # options( gpt3, bard )
analysisType = "classification" # options( summarization, classification )
outputLanguage = "pt-br" # options ( all? )
##########################################

try:
    transcribedAudio = TranscribeAudio("tiny", f"./{videoPath}")
    prompt = transcribedAudio.transcription_result
    
    if (modelAI == "gpt3"):
        config = {
            "model":"gpt-3.5-turbo",
            "token": os.getenv("API_KEY"),
            "outputLanguage":"portugues"
        }
        handler = chatgptHandler(config, prompt)
        handler.sendMessage()
        print(handler.summary)

    elif (modelAI == "bard"):
        print("Está demorando?")
        handler = bardHandler()
        handler.defineAnalysisType(analysisType, outputLanguage)
        #prompt = input("Enter Your Prompt: ")
        response = handler.get_bard_response(prompt)
        print(response)

except Exception as e:
    print(e)
>>>>>>> 59f99584b7b62fc1283d915f3908e49650c3eae1
