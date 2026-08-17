# Extended Auth Token Resolution for `apikey-image-gen`

## When the Token is Missing
If the token is not found in the standard locations (`AUTH_TOKEN`, `~/.hermes-web-ui/.token`, `~/.hermes/dashboard/.token`), follow this workflow:

1. **Check Dashboard Logs**:
   - Run `hermes dashboard --status` to confirm the dashboard is running.
   - If running, inspect the logs for token-related output. Example:
     ```bash
     grep -i "token\|auth" ~/.hermes/logs/dashboard.log
     ```

2. **User Provided Token**:
   - If the token is not found, request it from the user. Example:
     ```
     Big Brother, I couldn't find the Hermes Web UI auth token. Could you provide it or guide me on how to obtain it?
     ```

3. **Manual Token File Creation**:
   - If the user provides the token, save it to one of the expected paths:
     ```bash
     echo "<token>" > ~/.hermes-web-ui/.token
     ```

## Pitfalls
- **Dashboard Not Running**: If `hermes dashboard --status` shows no processes, start the dashboard using `hermes dashboard`.
- **Permission Issues**: Ensure the token file is readable by the Hermes process. Example:
  ```bash
  chmod 600 ~/.hermes-web-ui/.token
  ```

## Provider Configuration
The `apikey-image-gen` skill requires the `fun-codex` provider to be configured in `config.yaml`. Example:

```yaml
custom_providers:
  - name: fun-codex
    base_url: https://api.apikey.fun/v1
    api_key: YOUR_API_KEY_HERE
    model: gpt-5.5
    api_mode: codex_responses
```

If the provider is missing, the skill will return `missing_fun_codex_provider`. Request the API key from the user and update `config.yaml`.