from fastapi import APIRouter, UploadFile, File
from pydantic import BaseModel
from config.ProgramConfig import Config
from secrets import token_hex
from typing import Optional
from pipeline.pipeline import Pipeline

router = APIRouter(prefix="/summarize-video")
  
class SummarizeVideoResponse(BaseModel):
  summary: str

async def uploadVideo(file: Optional[UploadFile] = File(None)):
  if file:
    file_ext = file.filename.split(".").pop()
    file_name = token_hex(10)
    file_path = f"{file_name}.{file_ext}"
    with open(file_path, "wb") as f:
      content = await file.read()
      f.write(content)

@router.post("/", response_model=SummarizeVideoResponse, status_code=200)
async def get_video_summary(config: Config):
  try:
    pipeline = Pipeline(config)
    res = pipeline.summarize()
    return {"sucess":True, "summary":res}
  except Exception as e:
    print(e)