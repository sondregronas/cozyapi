import json
import random
from dataclasses import dataclass, field
from pathlib import Path

from __init__ import NEGATIVE_PROMPT

# Load default model
DEFAULT_MODEL = "flux1-dev-fp8.json"
with open(Path("workflows") / DEFAULT_MODEL, "r") as f:
    DEFAULT_WORKFLOW = json.load(f)


@dataclass
class ImageRes:
    width: int = 512
    height: int = 512


@dataclass
class ComfySettings:
    seed: int = -1  # -1 for random seed
    steps: int = 50
    res: ImageRes = field(default_factory=ImageRes)

    def __post_init__(self):
        if self.seed == -1:
            self.seed = random.randint(0, 2**32 - 1)


@dataclass
class Workflow:
    prompt: str
    negative_prompt: str = "low resolution, bad anatomy, blurry"
    settings: ComfySettings = field(default_factory=ComfySettings)
    workflow: dict = field(default_factory=lambda: DEFAULT_WORKFLOW)
    _enforced_negative_prompt: str = field(default_factory=lambda: NEGATIVE_PROMPT)

    def __post_init__(self):
        negative_prompt = self.negative_prompt.strip()
        negative_prompt += "" if not negative_prompt else ", "
        negative_prompt += self._enforced_negative_prompt

        # Avoid mutating the default workflow
        self.workflow = self.workflow.copy()
        # Hardcoded values for now
        self.workflow["6"]["inputs"]["text"] = self.prompt
        self.workflow["33"]["inputs"]["text"] = negative_prompt
        self.workflow["31"]["inputs"]["seed"] = self.settings.seed
        self.workflow["31"]["inputs"]["steps"] = self.settings.steps
        self.workflow["27"]["inputs"]["width"] = self.settings.res.width
        self.workflow["27"]["inputs"]["height"] = self.settings.res.height
