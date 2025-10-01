import json
import random
from dataclasses import dataclass, field

from __init__ import NEGATIVE_PROMPT, WORKFLOW_PATH
from nodemap import NODE_MAP

# Load default model
with open(WORKFLOW_PATH, "r") as f:
    WORKFLOW = json.load(f)


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
    workflow: dict = field(default_factory=lambda: WORKFLOW)
    _enforced_negative_prompt: str = field(default_factory=lambda: NEGATIVE_PROMPT)

    def __post_init__(self):
        negative_prompt = self.negative_prompt.strip()
        negative_prompt += "" if not negative_prompt else ", "
        negative_prompt += self._enforced_negative_prompt

        # Avoid mutating the default workflow
        self.workflow = self.workflow.copy()

        key = [key for key in NODE_MAP if WORKFLOW_PATH.name in key][0]
        n = NODE_MAP.get(key, NODE_MAP["default"])

        self.workflow[n.prompt[0]]["inputs"][n.prompt[1]] = self.prompt
        self.workflow[n.nprompt[0]]["inputs"][n.nprompt[1]] = negative_prompt
        self.workflow[n.seed[0]]["inputs"][n.seed[1]] = self.settings.seed
        self.workflow[n.steps[0]]["inputs"][n.steps[1]] = self.settings.steps
        self.workflow[n.width[0]]["inputs"][n.width[1]] = self.settings.res.width
        self.workflow[n.height[0]]["inputs"][n.height[1]] = self.settings.res.height
