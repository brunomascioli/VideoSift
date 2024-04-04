from fastapi import APIRouter
from pydantic import BaseModel
from enum import Enum
from transcribe_audio_to_text import TranscribeAudio
import LLMs

router = APIRouter(prefix="/summarize-video")

class WhisperSize(str, Enum):
  small = "small"
  medium = "medium"
  large = "large"

class LlmModel(str, Enum):
  gemini = "gemini"
  gpt3 = "gpt-3.5"

class SummarizeVideoRequest(BaseModel):
  video_url: str
  whisper_size: WhisperSize
  llm_model: str
  api_token: str
  
class SummarizeVideoResponse(BaseModel):
  summary: str

@router.post("/", response_model=SummarizeVideoRequest, status_code=200)
def get_video_summary(config: SummarizeVideoResponse):
  tran

  return SummarizeVideoResponse(summary=summary)
