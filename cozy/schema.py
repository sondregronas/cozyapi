from enum import Enum
from typing import Optional

from fastapi import Query, Body
from pydantic import BaseModel

from __init__ import MAX_RESOLUTION, MAX_STEPS


class ImageSize(str, Enum):
    Square = "square"
    Portrait = "portrait"
    Landscape = "landscape"


imagerequest_body = Body(
    ...,
    examples=[
        {
            "prompt": "A cozy cabin in the woods made of gingerbread",
            "negative_prompt": "low resolution, blurry",
            "width": 768,
            "height": 512,
            "steps": 25,
        },
    ],
)


class ImageRequest(BaseModel):
    prompt: str = Query(
        ...,
        min_length=1,
        max_length=10000,
        description="The prompt to generate an image for.",
        example="A cozy cabin in the woods made of gingerbread",
    )
    negative_prompt: Optional[str] = Query(
        "",
        max_length=10000,
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
        le=MAX_RESOLUTION,
        description="Overrides the default width determined by `size`.",
        example=None,
    )
    height: Optional[int] = Query(
        default=None,
        ge=16,
        le=MAX_RESOLUTION,
        description="Overrides the default height determined by `size`.",
        example=None,
    )
    steps: Optional[int] = Query(
        default=25,
        ge=1,
        le=MAX_STEPS,
        description="More steps equals better quality, but takes longer.",
        example=25,
    )
    seed: Optional[str | int] = Query(
        default=None,
        description="Will be used as the seed for image generation (Default: random).",
        example=None,
    )
