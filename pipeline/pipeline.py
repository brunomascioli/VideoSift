from LLMs.gpt3 import ChatgptHandler
from LLMs.gemini import GeminiHandler
from transcribe.transcribe_audio_to_text import TranscribeAudio
from config.ProgramConfig import *

class Pipeline():
    def __init__(self, config) -> None:
        self.config = config
        self.llm_model = config.llm_model
        self.model_size = config.whisper_size
        self.video_url = config.video_url
        self.file = config.file

    async def summarize(self) -> str:       
        transcription = await TranscribeAudio(self.model_size, self.video_url, self.file).process()

        if self.llm_model == LlmModel.gpt3:
            llm_response = ChatgptHandler(self.config, transcription).sendMessage()
            return llm_response.getSummary()
        
        if self.llm_model == LlmModel.gemini:
            llm_response = GeminiHandler(self.config, transcription)
            return llm_response.getSummary() 
        