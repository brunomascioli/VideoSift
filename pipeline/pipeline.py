from LLMs.gpt3 import ChatGptHandler
from LLMs.gemini import GeminiHandler
from typing import AsyncGenerator
from transcribe.transcribe_audio_to_text import TranscribeAudio
from config.ProgramConfig import *

class Pipeline():
    def __init__(self, config) -> None:
        self.config = config
        self.llm_model = config.llm_model
        self.model_size = config.whisper_size
        self.video_url = config.video_url
        self.file = config.file

    async def summarize(self) -> AsyncGenerator:     
        transcribe_audio_process = TranscribeAudio(self.model_size, self.video_url, self.file).process        
        
        transcription = []
        async for transcribe_event in transcribe_audio_process(transcription):
            yield transcribe_event
        if self.llm_model == LlmModel.gpt3:
            yield {"status": "Processing completed"}
            gpt_handler = ChatGptHandler(self.config, transcription[0]).send_message()
            gpt_handler.send_message()
            llm_response = gpt_handler.get_summary()
        elif self.llm_model == LlmModel.gemini:
            yield {"status": "Processing with gemini"}
            with open("transcription.txt", "r") as f:
                f.write(transcription[0])
            gemini_handler = GeminiHandler(self.config, transcription[0])
            gemini_handler.send_message()
            llm_response = gemini_handler.get_summary()
            with open("summarization.txt", "w") as f:
                f.write(llm_response)
            print(llm_response)
    
        yield {"status": "completed", "summary": llm_response}      