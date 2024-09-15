from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pytube import YouTube
from pathlib import Path

app = FastAPI()

# Directory to store downloaded files
DOWNLOAD_DIR = Path("downloads")
DOWNLOAD_DIR.mkdir(exist_ok=True)

# Serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def index():
    return FileResponse("static/index.html")

@app.post("/download")
async def download_video(request: Request):
    data = await request.json()
    video_url = data.get("videoUrl")
    format = data.get("format")

    if not video_url:
        raise HTTPException(status_code=400, detail="Invalid video URL")

    try:
        yt = YouTube(video_url)
        
        if format == 'mp4':
            stream = yt.streams.get_highest_resolution()
        elif format == 'mp3':
            stream = yt.streams.filter(only_audio=True).first()
        else:
            raise HTTPException(status_code=400, detail="Invalid format selected")

        file_path = stream.download(output_path=DOWNLOAD_DIR)
        
        return JSONResponse(content={"file": file_path})

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    