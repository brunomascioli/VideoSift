import uvicorn
from fastapi import FastAPI, UploadFile, File
from summarize_video.routers import summarize_video_router

app = FastAPI()

@app.get("/")
def main():
  return {"message", "teste"}

app.include_router(summarize_video_router.router)

if __name__ == '__main__':
  uvicorn.run(app, host="127.0.0.1", port=8000)