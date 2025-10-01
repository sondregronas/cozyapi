from dataclasses import dataclass


@dataclass
class NodeMap:
    prompt: tuple[str, str]
    nprompt: tuple[str, str]
    seed: tuple[str, str]
    steps: tuple[str, str]
    width: tuple[str, str]
    height: tuple[str, str]


NODE_MAP = {
    ("flux1-dev-fp8.json", "flux1-schnell-fp8.json"): NodeMap(
        prompt=("6", "text"),
        nprompt=("33", "text"),
        seed=("31", "seed"),
        steps=("31", "steps"),
        width=("27", "width"),
        height=("27", "height"),
    ),
}
NODE_MAP["default"] = NODE_MAP[("flux1-dev-fp8.json", "flux1-schnell-fp8.json")]
