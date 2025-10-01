# CozyAPI

A preliminary API to generate images using ComfyUI without messing with nodes by eliminating the ability to customize the workflow. 

> [!WARNING]
> This is **NOT** a replacement for ComfyUI, but a way to give a bit more controlled access to image generation without giving full access to the ComfyUI instance.

> [!NOTE]
> Current configured workflow requires the [ComfyUI-Unload-Model](https://github.com/SeanScripts/ComfyUI-Unload-Model) custom node

## Limitations

Image generation can take a while, and requests can time out unless you increase the timeout limit in your HTTP client (or proxy). For Nginx you can add `proxy_read_timeout 1800s;` to be safe. There's no way to "resume" a request (at the moment).

Not many workflows / models are supported, you will have to tweak stuff yourself if you want to do something fancy.

## Setup

See the `docker-compose.yml` and `.env.example` for more options.

```yaml
services:
  cozy:
    image: ghcr.io/sondregronas/cozyapi:latest
    container_name: cozy
    ports:
      - "8000:8000"
    environment:
      - COMFY_SERVER=127.0.0.1:8188
      - USE_SSL=false
      - MAX_RESOLUTION=1024
      - MAX_STEPS=40
    restart: unless-stopped
```