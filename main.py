import uvicorn
from fastapi import FastAPI
from summarize_video.routers import summarize_video_router

app = FastAPI()

@app.get("/")
async def summarize_url_video() -> str:
    return "Testando..."

app.include_router(summarize_video_router.router)

if __name__ == '__main__':
  uvicorn.run(app, host="0.0.0.0", port=8001)
