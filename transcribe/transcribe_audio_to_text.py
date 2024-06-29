import whisper
from pytube import YouTube
from enum import Enum
from secrets import token_hex
from typing import Optional
from fastapi import UploadFile
import torch
import tempfile
import os

class PathType(Enum):
    YOUTUBE = 0
    FILE = 1
    
class TranscribeAudio:
    def __init__(self, model_size, path, file: Optional[UploadFile] = None):
        self.model_size = model_size
        self.path = path
        self.local_path = path
        self.file = file
        self.path_type = None

    def _getPathType(self):
        if self.path.startswith("https://www.youtube.com/watch?v="):
            self.path_type = PathType.YOUTUBE
        else:
            self.path_type = PathType.FILE
    
    async def _download(self):
        if self.path_type == PathType.YOUTUBE:
            self._download_youtube_video()
        if self.path_type == PathType.FILE:
            await self._download_mp3()

    def _download_youtube_video(self):
        try:
            yt = YouTube(self.path)
            stream = yt.streams.filter(only_audio=True)

            # Cria um arquivo temporário
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp_file:
                filename = tmp_file.name
                stream[0].download(output_path=os.path.dirname(filename), filename=os.path.basename(filename))
                self.local_path = filename
                print(self.local_path)

        except Exception as e:
            raise Exception(f"Error downloading YouTube video! {str(e)}")

    
    async def _download_mp3(self):
        if not self.file:
            raise ValueError("No file provided")

        with tempfile.NamedTemporaryFile(delete=False, suffix=f".mp3") as tmp_file:
            content = await self.file.read()
            tmp_file.write(content)
            self.local_path = tmp_file.name

    def _perform_transcription(self):
        try:
            device = 'cuda' if torch.cuda.is_available() else 'cpu'
            model = whisper.load_model(self.model_size, device=device)
            result = model.transcribe(self.local_path)
            
            return result["text"]
        except Exception as e:
            raise Exception(f"Error during transcription! {str(e)}")

    def _delete_local_video(self):
        if self.local_path:
            try:
                os.remove(self.local_path)
            except Exception as e:
                print(f"Error deleting local video file: {str(e)}")

    async def process(self):
        self._getPathType()
        await self._download()
        
        if self.path_type == PathType.YOUTUBE: 
            text_result = self._perform_transcription()
        if self.path_type == PathType.FILE: 
            text_result = self._perform_transcription()
        
        self._delete_local_video()
        return text_result