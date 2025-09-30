import json
import random
from dataclasses import dataclass, field

from pathlib import Path

# Load default model
DEFAULT_MODEL = "flux1-dev-fp8.json"
with open(Path("workflows") / DEFAULT_MODEL, "r") as f:
    DEFAULT_WORKFLOW = json.load(f)


@dataclass
class ImageSize:
    width: int = 512
    height: int = 512


@dataclass
class ComfySettings:
    seed: int = -1  # -1 for random seed
    steps: int = 40
    size: ImageSize = field(default_factory=ImageSize)

    def __post_init__(self):
        if self.seed == -1:
            self.seed = random.randint(0, 2**32 - 1)


@dataclass
class Workflow:
    prompt: str
    negative_prompt: str = "low resolution, bad anatomy, blurry"
    settings: ComfySettings = field(default_factory=ComfySettings)
    workflow: dict = field(default_factory=lambda: DEFAULT_WORKFLOW)
    _enforced_negative_prompt: str = (
        "nudity, violence, gore, blood, sexual content, explicit, offensive"
    )

    def __post_init__(self):
        # Avoid mutating the default workflow
        self.workflow = self.workflow.copy()
        # Hardcoded values for now
        self.workflow["6"]["inputs"]["text"] = self.prompt
        self.workflow["33"]["inputs"]["text"] = (
            f"{self.negative_prompt}, {self._enforced_negative_prompt}"
        )
        self.workflow["31"]["inputs"]["seed"] = self.settings.seed
        self.workflow["31"]["inputs"]["steps"] = self.settings.steps
        self.workflow["27"]["inputs"]["width"] = self.settings.size.width
        self.workflow["27"]["inputs"]["height"] = self.settings.size.height
