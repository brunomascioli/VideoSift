from pydantic import BaseModel
from enum import Enum
from typing import Optional
from fastapi import UploadFile

class PathType(Enum):
  YOUTUBE = 0
  FILE = 1

class WhisperSize(str, Enum):
  tiny = "tiny"
  base = "base"
  small = "small"
  medium = "medium"
  large = "large"

class LlmModel(str, Enum):
  gemini = "gemini"
  gpt3 = "gpt3"

class TextProcessingOption(str, Enum):
  summarize = "summarize"
  classify = "classify"

class ConfigModel(BaseModel):
  file: Optional[UploadFile]
  video_url: Optional[str]
  api_token: str
  whisper_size: WhisperSize
  llm_model: LlmModel
  text_processing_option: TextProcessingOption
