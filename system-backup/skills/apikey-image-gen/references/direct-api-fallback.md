# Direct API Fallback for Image Generation

When the `image_gen` tool is unavailable or the `fun-codex` provider is misconfigured, use direct API calls to Stability AI or OpenAI as a fallback.

## Stability AI

### Text-to-Image

```bash
curl -X POST "https://api.stability.ai/v1/generation/stable-diffusion-xl-1024-v1-0/text-to-image" \
  -H "Authorization: Bearer $STABILITY_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "text_prompts": [{"text": "cyberpunk city at night, neon lights reflecting on rain-soaked streets"}],
    "cfg_scale": 7,
    "height": 1024,
    "width": 1024,
    "samples": 1,
    "steps": 30
  }' \
  --output output.png
```

### Python Example

```python
import requests
import json

api_key = "your_stability_ai_api_key"
prompt = "cyberpunk city at night, neon lights reflecting on rain-soaked streets"
url = "https://api.stability.ai/v1/generation/stable-diffusion-xl-1024-v1-0/text-to-image"

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

data = {
    "text_prompts": [{"text": prompt}],
    "cfg_scale": 7,
    "height": 1024,
    "width": 1024,
    "samples": 1,
    "steps": 30
}

response = requests.post(url, headers=headers, data=json.dumps(data))

if response.status_code == 200:
    with open("output.png", "wb") as f:
        f.write(response.content)
    print("Image saved as output.png")
else:
    print(f"Error: {response.status_code}, {response.text}")
```

## OpenAI

### Text-to-Image

```bash
curl -X POST "https://api.openai.com/v1/images/generations" \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "cyberpunk city at night, neon lights reflecting on rain-soaked streets",
    "n": 1,
    "size": "1024x1024"
  }' \
  --output output.png
```

### Python Example

```python
import requests
import json

api_key = "your_openai_api_key"
prompt = "cyberpunk city at night, neon lights reflecting on rain-soaked streets"
url = "https://api.openai.com/v1/images/generations"

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

data = {
    "prompt": prompt,
    "n": 1,
    "size": "1024x1024"
}

response = requests.post(url, headers=headers, data=json.dumps(data))

if response.status_code == 200:
    image_url = response.json()["data"][0]["url"]
    image_response = requests.get(image_url)
    with open("output.png", "wb") as f:
        f.write(image_response.content)
    print("Image saved as output.png")
else:
    print(f"Error: {response.status_code}, {response.text}")
```

## Pitfalls

- **API Key Exposure**: Never hardcode API keys in scripts or commands. Use environment variables or secure credential stores.
- **Rate Limits**: Free-tier API keys often have strict rate limits. Monitor usage and implement retries with exponential backoff.
- **Output Handling**: Always verify the response status code and handle errors gracefully. Stability AI and OpenAI return different response formats — ensure your script parses them correctly.
- **File Paths**: Use absolute paths for output files to avoid permission issues or unexpected save locations.