# 9Router Provider Quirks

## Overview
9Router is a **local AI infrastructure manager** that proxies requests to multiple providers (Gemini, FLUX, MiniMax, etc.) behind a single OpenAI-compatible endpoint. It runs on `localhost:20128` and does not require an API key for local use.

## Key Quirks

### 1. Audio Input Support
- **Format**: Accepts `input_audio` in base64-encoded `ogg`, `mp3`, or `wav`.
- **Payload Example**:
  ```json
  {
    "model": "gemini/gemini-3.6-flash",
    "messages": [{"role": "user", "content": [
      {"type": "text", "text": "Transcribe this audio."},
      {"type": "input_audio", "input_audio": {"data": "<base64>", "format": "ogg"}}
    ]}]
  }
  ```
- **Use Case**: Speech-to-text, voice message transcription.

### 2. Model Discovery
- **Endpoint**: `GET /v1/models`
- **Response**: Lists available models and their capabilities (e.g., `audioInput`, `vision`).
- **Example**:
  ```bash
  curl http://localhost:20128/v1/models
  ```

### 3. Local-Only Access
- **Binding**: `localhost` only — no remote access.
- **Verification**: Check if the service is running:
  ```bash
  curl -s http://localhost:20128/dashboard | grep "9Router Proxy"
  ```

### 4. No API Key Required
- **Authentication**: None for local use.
- **Security**: Ensure the machine is not exposed to untrusted networks.

### 5. Provider-Specific Models
- **Gemini**: `gemini/gemini-3.6-flash`, `gemini/gemini-3.5-flash-lite`
- **FLUX**: `flux/flux-schnell`, `flux/flux-dev`
- **MiniMax**: `abab6.5-chat`

## Pitfalls

- **Base64 Encoding**: Audio files must be base64-encoded before sending. Use Python or `base64` CLI:
  ```bash
  base64 -w 0 audio.ogg > audio.b64
  ```
- **Model Capabilities**: Not all models support `input_audio` or `vision`. Check `/v1/models` first.
- **Local Dependencies**: 9Router requires local setup (Docker, Python, or binary).
- **No Streaming**: Audio input is **not streamed** — send the full file in one request.