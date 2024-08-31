from fastapi import APIRouter, UploadFile, Form, HTTPException, Request
from fastapi.responses import StreamingResponse
from config.ProgramConfig import *
from typing import Optional, AsyncIterable
from pipeline.pipeline import Pipeline
from asyncio import sleep
import json, tempfile

router = APIRouter(prefix="/summarize-video")

@router.post("/", status_code=200)
async def get_video_summary(
  request: Request,
  file: Optional[UploadFile] = None,
  video_url: Optional[str] = Form(None),
  api_token: str = Form(...),
  whisper_size: WhisperSize = Form(...),
  llm_model: LlmModel = Form(...),
  text_processing_option: TextProcessingOption = Form(...)
):
  config = ConfigModel(
    file=file,
    video_url=video_url,
    api_token=api_token,
    whisper_size=whisper_size,
    llm_model=llm_model,
    text_processing_option=text_processing_option
  )

  if not (file or video_url):
    raise HTTPException(status_code=400, detail="Either 'file' or 'video_url' must be provided.")

  if file and video_url:
    raise HTTPException(status_code=400, detail="Only one of 'file' or 'video_url' must be provided.")

  if file and not file.content_type.startswith("video"):
    raise HTTPException(status_code=400, detail="Invalid file type. Must be a video file.")

  try:
    
    if file: 
      with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp_file:
        content = await file.read()
        tmp_file.write(content)
        tmp_path = tmp_file.name
        config.video_url = tmp_path

    pipeline = Pipeline(config)

    print("Starting summarization")
    async def event_generator() -> AsyncIterable[str]:
      async for update in pipeline.summarize():
        print(update)
        if await request.is_disconnected():
          break
        yield json.dumps(update)
        await sleep(0.1) 

    return StreamingResponse(event_generator(), media_type="text/event-stream")
  except Exception as e:
    raise HTTPException(status_code=500, detail=str(e))