from pydantic import BaseModel
from enum import Enum, auto

class WhisperSize(str, Enum):
  tiny = "tiny"
  base = "base"
  small = "small"
  medium = "medium"
  large = "large"

class LlmModel(str, Enum):
  gemini = "gemini"
  gpt3 = "gpt3"

class Config(BaseModel):
    video_url: str
    api_token: str
    whisper_size: WhisperSize
    llm_model: LlmModel
