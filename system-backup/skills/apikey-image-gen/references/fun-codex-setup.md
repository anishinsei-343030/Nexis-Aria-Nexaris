# Fun-Codex Provider Setup

## Adding the Provider to `config.yaml`
If the `fun-codex` provider is missing from `config.yaml`, add it under the `custom_providers` section:

```yaml
custom_providers:
  - name: fun-codex
    base_url: https://api.apikey.fun/v1
    api_key: YOUR_API_KEY_HERE
    model: gpt-5.5
    api_mode: codex_responses
```

Replace `YOUR_API_KEY_HERE` with the actual API key for `api.apikey.fun`.

## Troubleshooting "Unauthorized" Errors
If the Hermes Web UI endpoint (`/api/hermes/media/apikey-image-generate`) returns "Unauthorized" even with `auth` disabled:

1. **Check for a Hermes Web UI Token**
   The endpoint may still require a bearer token. Look for it in:
   - `~/.hermes-web-ui/.token`
   - `~/.hermes/dashboard/.token`
   - The dashboard logs (`hermes dashboard --status`)

2. **Manually Generate a Token**
   If the token is missing, you can:
   - Restart the dashboard with `hermes dashboard --generate-token` (if supported).
   - Ask the user to provide the token.

3. **Verify the `fun-codex` Provider**
   Ensure the provider is correctly configured in `config.yaml` and the API key is valid.

## Example `curl` Command
```bash
curl -X POST "http://127.0.0.1:9119/api/hermes/media/apikey-image-generate" \
  -H "Authorization: Bearer YOUR_HERMES_WEB_UI_TOKEN" \
  -H "Content-Type: application/json" \
  -H "X-Hermes-Profile: default" \
  -d '{
    "mode": "text",
    "prompt": "A high-quality anime-style portrait of Celestia Mei Nexaris",
    "size": "1024x1024",
    "output_path": "/absolute/path/to/output.png"
  }'
```