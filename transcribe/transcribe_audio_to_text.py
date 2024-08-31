from typing import Optional, AsyncGenerator
from fastapi import UploadFile
import torch
import tempfile
import os
import whisper
from config.ProgramConfig import PathType
from pytubefix import YouTube
from pyannote.audio import Pipeline
from dotenv import dotenv_values
from transcribe.diarize import process_diarized_text

class TranscribeAudio:
    def __init__(self, model_size: str, path: str, file: Optional[UploadFile] = None):
        self.model_size = model_size
        self.path = path
        self.local_path = path
        self.file = file
        self.path_type = self._get_path_type()
        self.device = self._set_device()
        self.model = whisper.load_model(self.model_size, device=self.device)

    def _set_device(self):
        return "cuda" if torch.cuda.is_available() else "cpu"

    def _get_path_type(self) -> None:
        print(self.path)
        if self.path.startswith("https://www.youtube.com/watch?v="):
            return PathType.YOUTUBE
        else:
            return PathType.FILE
    
    async def _download(self) -> None:
        if self.path_type == PathType.YOUTUBE:
            self.local_path = self._download_youtube_video()
        elif self.path_type == PathType.FILE:
            self.local_path = self.path
        else:
            raise ValueError("Invalid path type")

    def _download_youtube_video(self) -> str:
        try:
            yt = YouTube(self.path)
            stream = yt.streams.filter.get_audio_only()
            if not stream:
                raise Exception("No audio stream found")
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp_file:
                stream.download(output_path=os.path.dirname(tmp_file.name), filename=os.path.basename(tmp_file.name), )
                return tmp_file.name
            
        except Exception as e:
            raise Exception(f"Error downloading YouTube video! {str(e)}")

    async def _download_mp3(self) -> str:
        if not self.file:
            raise ValueError("No file provided")

        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp_file:
            content = await self.file.file.read()
            tmp_file.write(content)
            return tmp_file.name
    
    def _perform_transcription(self) -> str:
        try:
            env = dotenv_values()
            model = whisper.load_model(self.model_size, device=self.device)
            transcription = model.transcribe(self.local_path)
            pipeline = Pipeline.from_pretrained(
                "pyannote/speaker-diarization-3.0",
                use_auth_token=env["HUGGINGFACE_TOKEN"]
            )
            
            diarization_result = pipeline(self.local_path)
            final_result = process_diarized_text(diarization_data=diarization_result,
                                                  transcription_data=transcription)
            return final_result
        except Exception as e:
            raise Exception(f"Error during transcription! {str(e)}")

    def _delete_local_file(self, path: str) -> None:
        try:
            os.remove(path)
        except Exception as e:
            print(f"Error deleting local file: {str(e)}")

    async def process(self, transcription) -> AsyncGenerator:
        yield {"status": "Downloading video..."}
        await self._download()
        yield {"status": "Transcribing video..."}
        try:
            text_result = self._perform_transcription()
            transcription.append(text_result)
        finally:
            self._delete_local_file(self.local_path)
