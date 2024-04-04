import whisper
from pytube import YouTube
import torch

# path_type = {youtube = 0}

class TranscribeAudio:
    def __init__(self, model_size, file_path):
        self.model_size = model_size
        self.file_path = file_path
        self.path_type
        self.transcription_result = self.perform_transcription()

    
    def getPathType(self):
        if self.file_path.startswith("https://www.youtube.com/watch?v="):
            self.downloadYoutubeVideo()

    def perform_transcription(self):
        device = 'cuda' if torch.cuda.is_available() else 'cpu'
        model = whisper.load_model(self.model_size, device=device)
        result = model.transcribe(self.file_path)
        return result["text"]
    
    def downloadYoutubeVideo(self):
        yt = YouTube(self.file_path)
        stream = yt.streams.filter(only_audio=True).all()
        stream[0].download("/videos")
    

transcription = TranscribeAudio("small", "videoTest").perform_transcription