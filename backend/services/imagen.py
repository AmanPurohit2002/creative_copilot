import asyncio
import base64
import urllib.parse
import urllib.request
import time

def fetch_dummy_image(width: int, height: int, seed: int) -> str:
    """Fetches a dummy placeholder image to bypass rate limits."""
    try:
        url = f"https://picsum.photos/seed/{seed}/{width}/{height}"
        req = urllib.request.Request(url, headers={'User-Agent': 'CreativeCopilot/1.0'})
        with urllib.request.urlopen(req) as response:
            image_bytes = response.read()
            return base64.b64encode(image_bytes).decode("utf-8")
    except Exception as e:
        raise Exception(f"Failed to fetch dummy image: {e}")

async def generate_all_panels(
    shots_with_prompts: list[dict],
    aspect_ratio: str = "16:9",
) -> list[dict]:
    """
    Assigns dummy placeholder images for all shots.
    """
    dims = {
        "16:9": (1024, 576), # Lower res for speed & stability
        "9:16": (576, 1024),
        "1:1": (1024, 1024),
    }.get(aspect_ratio, (1024, 576))
    width, height = dims
    
    panels = []

    for i, shot in enumerate(shots_with_prompts):
        prompt = shot.get("image_prompt", "")
        
        # Pollinations requires slower requests to stay on the free tier
        max_retries = 3
        for attempt in range(max_retries):
            try:
                seed = int(time.time() * 1000) + i
                b64 = await asyncio.to_thread(fetch_dummy_image, width, height, seed)
                shot["image_base64"] = b64
                shot["error"] = None
                break
            except Exception as e:
                print(f"Shot {i+1} image failed on attempt {attempt+1}: {e}")
                if "402" in str(e) or "429" in str(e):
                    # Rate limit or free tier warning, wait longer and retry
                    await asyncio.sleep(3)
                else:
                    shot["image_base64"] = None
                    shot["error"] = str(e)
                    break
        else:
            # If all retries fail
            shot["image_base64"] = None
            shot["error"] = "Image generation failed due to rate limiting."
            
        panels.append(shot)
        
        # Add a longer delay to prevent 402 Payment Required errors
        if i < len(shots_with_prompts) - 1:
            await asyncio.sleep(2.5)

    return panels
