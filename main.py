import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from summarize_video.routers import summarize_video_router

app = FastAPI()

origins = [
    "*", 
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins, 
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

app.include_router(summarize_video_router.router)

if __name__ == '__main__':
  uvicorn.run(app, host="localhost", port=8080)