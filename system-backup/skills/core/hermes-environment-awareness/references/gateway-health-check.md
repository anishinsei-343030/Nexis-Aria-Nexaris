# Gateway Health Check Reference

## Layered Verification Procedure

After a gateway restart or when Telegram connectivity is reported down.

### Layer 1: Process Status
```bash
# Check gateway process via Hermes CLI
hermes gateway status

# Expected output:
# ✓ Gateway process running (PID: 15076)
# ✓ Scheduled Task registered: Hermes_Gateway (Status: Ready)

# Check gateway_state.json
cat ~/.hermes/gateway_state.json
```

### Layer 2: Platform Connectivity
Check `gateway_state.json` → `platforms.telegram`:
```json
{
  "state": "connected",
  "error_code": null,
  "error_message": null
}
```

### Layer 3: Port Binding
```bash
# Check if HTTP listener is on expected port
netstat -ano | grep 7700

# If empty — the gateway may not expose an HTTP endpoint.
# Telegram polling works without it.
```

### Layer 4: Config Validation
```yaml
# Check ~/.hermes/config.yaml for telegram.token
telegram:
  token: "..."  # REQUIRED — missing token = bot can't auth
  allowed_chats: "-1003740504045,..."
```

### Layer 5: Log Review
```bash
# Recent gateway log entries
tail -30 ~/.hermes/logs/gateway.log

# Check for startup errors
grep -i "error\|fail\|traceback" ~/.hermes/logs/gateway.log
```

## Common Failure Patterns

### Missing `telegram.token`
- **Symptom**: Gateway runs (PID visible) but Telegram shows no bot messages.
- **Diagnosis**: `grep telegram.token ~/.hermes/config.yaml` returns nothing.
- **Fix**: Add `token: "<BOT_TOKEN>"` under `telegram:` in `config.yaml`, then restart gateway.

### Stale Gateway PID
- **Symptom**: `gateway_state.json` shows active PID but process is dead.
- **Fix**: `hermes gateway stop` (cleans stale lock), then `hermes gateway start`.

### Telegram API Error
- **Symptom**: `gateway_state.json` shows `"state": "error"` with `error_code`.
- **Fix**: Invalid token → regenerate bot token via @BotFather.

## Quick Health Check
```bash
hermes gateway status && python -c "import json; s=json.load(open(r'$HOME/.hermes/gateway_state.json')); print(f\"Telegram: {s['platforms']['telegram']['state']}\")"
```
