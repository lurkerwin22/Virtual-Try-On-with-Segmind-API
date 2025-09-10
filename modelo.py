import os
import time
import base64
import requests
from PIL import Image

# === Configuration ===
API_KEY = os.getenv("SEGMIND_API_KEY", "SG_df7a6586e3f59f08")  # Replace with your key if needed
API_URL = "https://api.segmind.com/v1/try-on-diffusion"
PERSON_IMAGE_PATH = "person.jpg"
CLOTHING_IMAGE_PATH = "clothing.png"
OUTPUT_IMAGE_PATH = "output.jpg"
MAX_RETRIES = 3

def preprocess_image(path: str, size=(768, 1024)):
    """Resize image to model-recommended size for stable results."""
    img = Image.open(path).convert("RGB")
    img = img.resize(size)
    img.save(path)
    return path

def encode_image_to_base64(path: str) -> str:
    """Encode image file as Base64 string."""
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

def generate_tryon(person_path, clothing_path, output_path):
    headers = {"x-api-key": API_KEY}

    # Preprocess inputs for compatibility
    preprocess_image(person_path)
    preprocess_image(clothing_path)

    payload = {
        "model_image": encode_image_to_base64(person_path),
        "cloth_image": encode_image_to_base64(clothing_path),
        "category": "Upper body",        # Options: "Upper body", "Lower body", "Dress"
        "num_inference_steps": 30,       # More steps = better detail
        "guidance_scale": 8,             # Higher = more faithful to input clothing
        "seed": 42,                      # Fixed seed for consistent outputs
        "base64": False                  # Receive raw JPEG
    }

    for attempt in range(1, MAX_RETRIES + 1):
        print(f"🚀 Attempt {attempt}/{MAX_RETRIES}...")
        resp = requests.post(API_URL, json=payload, headers=headers)

        if resp.status_code == 200:
            with open(output_path, "wb") as out:
                out.write(resp.content)
            print(f"✅ Saved try‑on image to {output_path}")
            return True

        if resp.status_code == 429:
            wait = int(resp.headers.get("Retry-After", 60))
            print(f"⚠️ Rate limited—waiting {wait}s...")
            time.sleep(wait)
            continue

        print(f"❌ Error {resp.status_code}: {resp.text}")
        break

    print("❌ All attempts failed.")
    return False

if __name__ == "__main__":
    if not os.path.exists(PERSON_IMAGE_PATH) or not os.path.exists(CLOTHING_IMAGE_PATH):
        print("❌ One or both image files are missing.")
    else:
        if generate_tryon(PERSON_IMAGE_PATH, CLOTHING_IMAGE_PATH, OUTPUT_IMAGE_PATH):
            img = Image.open(OUTPUT_IMAGE_PATH)
            img.show()
