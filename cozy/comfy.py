import io
import json
import uuid
from io import BytesIO

import aiohttp
import websockets

from __init__ import COMFY_SERVER, HTTP_SCHEME, WS_SCHEME
from workflow import Workflow


async def _queue_prompt(prompt, cid: str):
    async with aiohttp.ClientSession() as session:
        async with session.post(
            f"{HTTP_SCHEME}://{COMFY_SERVER}/prompt",
            json={"prompt": prompt, "client_id": cid},
        ) as resp:
            return await resp.json()


async def _gen_image(ws, workflow, cid: str):
    """Handle websocket messages and collect generated images."""
    prompt_id = (await _queue_prompt(workflow, cid=cid))["prompt_id"]
    current_node = ""
    output_images = dict()

    async for out in ws:
        if isinstance(out, str):
            message = json.loads(out)

            # We only care about "executing" messages (even though progress_state could do the same thing)
            if message["type"] != "executing":
                continue

            data = message["data"]

            # We only care about messages for our prompt
            if data["prompt_id"] != prompt_id:
                continue
            # We are done when node is None
            if data["node"] is None:
                break

            # Track the current node
            current_node = data["node"]

        # Store bytes from the websocket binary messages (not strings)
        else:
            if current_node != "save_image_websocket_node":
                continue
            images_output = output_images.get(current_node, [])
            images_output.append(out[8:])
            output_images[current_node] = images_output

    return output_images


async def generate_image(wf: Workflow) -> BytesIO:
    cid = str(uuid.uuid4())
    uri = f"{WS_SCHEME}://{COMFY_SERVER}/ws?clientId={cid}"
    async with websockets.connect(uri, max_size=10 * 1024 * 1024) as ws:
        await ws.send(json.dumps(wf.workflow))
        images = await _gen_image(ws, wf.workflow, cid=cid)

    return io.BytesIO(images["save_image_websocket_node"][0])
