from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

import comfy
from util import get_image_res, ImageSize
from workflow import Workflow, ComfySettings

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def index():
    return {"message": "Cozy API is running"}


class ImageRequest(BaseModel):
    prompt: str
    size: ImageSize = ImageSize.Landscape


@app.get("/generate", response_class=StreamingResponse)
async def get_generate_image(
    prompt: str, size: ImageSize = ImageSize.Landscape
) -> StreamingResponse:
    """Generate an image based on the provided prompt and size using query parameters."""
    settings = ComfySettings(res=get_image_res(size))
    workflow = Workflow(prompt=prompt, settings=settings)

    img = await comfy.generate_image(wf=workflow)
    return StreamingResponse(img, media_type="image/png")


@app.post("/generate", response_class=StreamingResponse)
async def post_generate_image(request: ImageRequest) -> StreamingResponse:
    """Generate an image based on the provided prompt and size using a JSON body."""
    settings = ComfySettings(res=get_image_res(size=request.size))
    workflow = Workflow(prompt=request.prompt, settings=settings)

    img = await comfy.generate_image(wf=workflow)
    return StreamingResponse(img, media_type="image/png")


if __name__ == "__main__":
    import os

    os.system("uvicorn api:app --reload")
