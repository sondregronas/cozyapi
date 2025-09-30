from enum import Enum
from typing import Optional

from fastapi import Query, Body
from pydantic import BaseModel

from workflow import ImageRes, ComfySettings, Workflow


class ImageSize(str, Enum):
    Square = "square"
    Portrait = "portrait"
    Landscape = "landscape"


imagerequest_body = Body(
    ...,
    examples=[
        {
            "prompt": "A cozy cabin in the woods made of gingerbread",
            "width": 512,
            "height": 512,
        },
    ],
)


class ImageRequest(BaseModel):
    prompt: str = Query(
        ...,
        min_length=1,
        max_length=3000,
        description="The prompt to generate an image for.",
        example="A cozy cabin in the woods made of gingerbread",
    )
    negative_prompt: Optional[str] = Query(
        "",
        max_length=3000,
        description="A negative prompt to avoid certain elements in the generated image.",
        example="low resolution, bad anatomy, blurry",
    )
    size: Optional[ImageSize] = Query(
        default=ImageSize.Landscape,
        description="Choose between 1:1, 2:3 or 3:2. 512px on the short side. Ignored if width and height are specified.",
    )
    width: Optional[int] = Query(
        default=None,
        ge=16,
        le=1024,
        description="Overrides the default width determined by `size`.",
        example=None,
    )
    height: Optional[int] = Query(
        default=None,
        ge=16,
        le=1024,
        description="Overrides the default height determined by `size`.",
        example=None,
    )

    seed: Optional[str | int] = Query(
        default=None,
        description="Will be used as the seed for image generation (Default: random).",
        example=None,
    )


def get_image_res(size: ImageSize) -> ImageRes:
    match size:
        case ImageSize.Square:
            return ImageRes(512, 512)
        case ImageSize.Portrait:
            return ImageRes(512, 768)
        case _:
            return ImageRes(768, 512)


def construct_workflow(
    request: ImageRequest,
) -> Workflow:
    size = request.size or ImageSize.Landscape
    width = request.width
    height = request.height
    seed = request.seed

    if request.width and request.height:
        settings = ComfySettings(res=ImageRes(width=width, height=height))
    else:
        settings = ComfySettings(res=get_image_res(size))

    if isinstance(seed, str):
        try:
            settings.seed = int(seed)
        except ValueError:
            settings.seed = abs(hash(seed)) % (10**8)

    return Workflow(
        prompt=request.prompt,
        negative_prompt=request.negative_prompt,
        settings=settings,
    )
