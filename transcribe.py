# ffmpeg https://www.geeksforgeeks.org/how-to-install-ffmpeg-on-windows/
import whisper
import torch

class TranscribeAudio:
    def __init__(self, model_size, file_path):
        self.model_size = model_size
        self.file_path = file_path
        self.transcription_result = self.perform_transcription()

    def perform_transcription(self):
        device = 'cuda' if torch.cuda.is_available() else 'cpu'
        print(device)
        model = whisper.load_model(self.model_size, device=device)
        result = model.transcribe(self.file_path)
        return result["text"]
