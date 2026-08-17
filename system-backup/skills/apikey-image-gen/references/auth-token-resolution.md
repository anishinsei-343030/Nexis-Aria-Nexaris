# Hermes Web UI Auth Token Resolution

## Where to Look
The Hermes Web UI (launched via `hermes dashboard`) uses a bearer token for authentication. This token is resolved in the following order:

1. **Environment Variable**: `AUTH_TOKEN`
2. **File Paths**:
   - `${HERMES_WEB_UI_HOME}/.token`
   - `${HERMES_WEBUI_STATE_DIR}/.token`
   - `~/.hermes-web-ui/.token`
   - `~/.hermes/dashboard/.token`

## How to Retrieve the Token
If the token is not found in the expected locations:

1. **Check Dashboard Logs**:
   - Run `hermes dashboard --status` to confirm the dashboard is running.
   - If running, check the logs for any token-related output.

2. **User Provided**:
   - If the token is not found, request it from the user. Example:
     ```
     Big Brother, I couldn't find the Hermes Web UI auth token. Could you provide it or guide me on how to obtain it?
     ```

3. **Manual Token File Creation**:
   - If the user provides the token, save it to one of the expected paths:
     ```bash
     echo "<token>" > ~/.hermes-web-ui/.token
     ```

## Troubleshooting
- **Dashboard Not Running**: Start it using `hermes dashboard`.
- **Token Not Found**: If the dashboard is running but the token is missing, the user may need to regenerate or locate it manually.
- **Permission Issues**: Ensure the token file is readable by the Hermes process.