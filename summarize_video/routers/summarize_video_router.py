from fastapi import APIRouter, UploadFile, File, Form
from pydantic import BaseModel
from config.ProgramConfig import *
from secrets import token_hex
from typing import Optional
from pipeline.pipeline import Pipeline

router = APIRouter(prefix="/summarize-video")
  
class SummarizeVideoResponse(BaseModel):
  summary: str

@router.post("/", status_code=200)
async def get_video_summary(
    file: Optional[UploadFile] = File(None),
    video_url: Optional[str] = Form(None),
    api_token: str = Form(...),
    whisper_size: WhisperSize = Form(...),
    llm_model: LlmModel = Form(...)
):
  if not file and not video_url:
    raise HTTPException(status_code=400, detail="Either 'file' or 'video_url' must be provided.")

  try:
    config = Config(
      file=file,
      video_url=video_url,
      api_token=api_token,
      whisper_size=whisper_size,
      llm_model=llm_model
    )
    if file: config.video_url = file.filename
    pipeline = Pipeline(config)
    res = await pipeline.summarize()
    return {"sucess":True, "summary":res }
  except Exception as e:
    raise HTTPException(status_code=500, detail=str(e))
    