from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse

import comfy
from schema import (
    imagerequest_body,
    construct_workflow,
    ImageRequest,
)

description = """
<h2>A simple API for generating images with ComfyUI</h2>

Made with ❤️ - source code available on <a href="https://github.com/sondregronas/cozyapi">GitHub</a>.
"""

app = FastAPI(
    title="Cozy API",
    description=description,
    version="0.1.0",
    openapi_tags=[
        {"name": "Image Generation", "description": "Endpoints for generating images"}
    ],
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/license/mit/",
    },
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", include_in_schema=False)
async def index():
    return {"message": "Cozy is running - visit the /docs to explore the API"}


@app.get(
    "/generate",
    response_class=StreamingResponse,
    name="Generate Image",
    tags=["Image Generation"],
)
async def get_generate_image(
    request: ImageRequest = Depends(),
) -> StreamingResponse:
    """
    Generate an image based on the provided prompt and size using query parameters.

    Returns PNG image bytes. Read the ImageRequest schema for details on query parameters.
    """
    workflow = construct_workflow(request)

    img = await comfy.generate_image(wf=workflow)
    return StreamingResponse(img, media_type="image/png")


@app.post(
    "/generate",
    response_class=StreamingResponse,
    name="Generate Image",
    tags=["Image Generation"],
)
async def post_generate_image(
    request: ImageRequest = imagerequest_body,
) -> StreamingResponse:
    """
    Generate an image based on the provided prompt and size using a JSON body.

    Returns PNG image bytes. Read the ImageRequest schema for details on body parameters.
    """
    return await get_generate_image(request)


if __name__ == "__main__":
    import os

    os.system("uvicorn api:app --reload")
