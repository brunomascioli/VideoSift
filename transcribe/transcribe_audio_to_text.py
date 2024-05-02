import whisper
from pytube import YouTube
from enum import Enum
import torch

class PathType(Enum):
    YOUTUBE = 0
    FILE = 1
    
class TranscribeAudio:
    def __init__(self, model_size, path):
        self.model_size = model_size
        self.path = path
        self.path_type = None
        self.local_path = None

    def _getPathType(self):
        if self.path.startswith("https://www.youtube.com/watch?v="):
            self.path_type = PathType.YOUTUBE
        else:
            self.path_type = PathType.FILE
    
    def _download(self):
        if self.path_type == PathType.YOUTUBE:
            self._downloadYoutubeVideo()

    def _downloadYoutubeVideo(self):
        try:    
            yt = YouTube(self.path)
            stream = yt.streams.filter(only_audio=True)
            stream[0].download(output_path=".", filename="downloaded_audio.mp4")
            self.local_path = f'./downloaded_audio.mp4'
        except Exception as e:
            raise Exception(f"Error downloading YouTube video! {str(e)}")

    def _perform_transcription(self):
        try:
            print(self.local_path)
            device = 'cuda' if torch.cuda.is_available() else 'cpu'
            model = whisper.load_model(self.model_size, device=device)
            result = model.transcribe(self.local_path)
            return result["text"]
        except Exception as e:
            raise Exception(f"Error during transcription! {str(e)}")

    def process(self):
        self._getPathType()
        if self.path_type != PathType.FILE: 
            self._download()
            return self._perform_transcription()
