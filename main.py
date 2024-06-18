import transcript_service
from fastapi import FastAPI, HTTPException
from urllib.parse import urlparse, parse_qs

app = FastAPI()


@app.get("/transcribes")
async def get_text(url: str):
    is_youtube = 'https://www.youtube.com/watch?v=' in url
    if not is_youtube:
        raise HTTPException(status_code=400, detail="Url должен начинаться с https://www.youtube.com/watch?v=")

    video_id = get_video_id(url)
    if not video_id:
        raise HTTPException(status_code=400, detail="Url должен содержать параметер v=")

    result = transcript_service.get_transcript_text(video_id)
    return result


def get_video_id(url):
    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)
    if 'v' in query_params:
        video_id = query_params['v'][0]
        return video_id
    else:
        return
