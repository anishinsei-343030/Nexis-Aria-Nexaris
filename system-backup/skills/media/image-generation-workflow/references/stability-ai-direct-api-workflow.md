# Stability AI Direct API Workflow

## Overview
This reference documents the workflow for generating images using the **Stability AI API** directly via `curl` or `execute_code`. This is useful when Hermes tools like `image_gen` are unavailable or when direct API control is required.

## Prerequisites
- **Stability AI API Key**: Must be set in the environment or `.env` file as `STABILITY_AI_API_KEY`.
- **Output Directory**: Must exist or be created before saving the image. Use:
  ```bash
  mkdir -p "D:/Hermes\Celestia mei Nexaris/assets/images"
  ```

## API Endpoint
```
https://api.stability.ai/v2beta/stable-image/generate/sd3
```

## Required Headers
- **Authorization**: `Bearer <STABILITY_AI_API_KEY>`
- **Accept**: `image/*` (required for image output)

## Request Structure
The API expects a **multipart/form-data** request with the following fields:
- **prompt**: The image generation prompt (e.g., "cosmic landscape, ultra-detailed, 8K").
- **output_format**: The output format (e.g., `png`).

## Example: `curl` Command
```bash
mkdir -p "D:/Hermes\Celestia mei Nexaris/assets/images" && \
curl -X POST "https://api.stability.ai/v2beta/stable-image/generate/sd3" \
-H "authorization: Bearer *** \
-H "accept: image/*" \
-F "prompt=A breathtaking cosmic landscape with swirling nebulas, iridescent stardust, and a lone futuristic spire reaching towards a binary star system, ultra-detailed, digital art, 8K resolution, ethereal lighting" \
-F "output_format=png" \
--output "D:/Hermes\Celestia mei Nexaris/assets/images/cosmic_spire.png"
```

## Example: Python (`execute_code`)
```python
import requests
import os

API_KEY=***  # Replace with the actual key or fetch from environment
prompt = "A breathtaking cosmic landscape with swirling nebulas, iridescent stardust, and a lone futuristic spire reaching towards a binary star system, ultra-detailed, digital art, 8K resolution, ethereal lighting"
url = "https://api.stability.ai/v2beta/stable-image/generate/sd3"
save_dir = r"D:\\Hermes\Celestia mei Nexaris\\assets\\images"
save_path = os.path.join(save_dir, "cosmic_spire.png")

if not os.path.exists(save_dir):
    os.makedirs(save_dir)

headers = {
    "authorization": f"Bearer {API_KEY}",
    "accept": "image/*"
}
files = {
    "none": None  # Required for multipart form
}
data = {
    "prompt": prompt,
    "output_format": "png"
}

response = requests.post(url, headers=headers, files=files, data=data)

if response.status_code == 200:
    with open(save_path, "wb") as f:
        f.write(response.content)
    print(f"Successfully generated image and saved to {save_path}")
else:
    print(f"Error: {response.status_code}")
    print(response.text)
```

## Pitfalls
1. **401 Unauthorized**: Ensure the API key is correct and passed in the `authorization` header.
2. **Environment Variables in `execute_code`**: The `execute_code` sandbox may not have access to environment variables. Pass the key directly or use `curl`.
3. **Directory Creation**: Always create the output directory before saving the image.
4. **Absolute Paths**: Use absolute paths for output files to avoid ambiguity.

## Post-Generation Steps
1. **Send the image to the user immediately**:
   ```bash
   send_message action="send" target="telegram" message="MEDIA:D:/Hermes\Celestia mei Nexaris/assets/images/cosmic_spire.png"
   ```
2. **Verify the file exists**:
   ```bash
   ls -l "D:/Hermes\Celestia mei Nexaris/assets/images/cosmic_spire.png"
   ```