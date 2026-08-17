# Telegram Delivery Verification (worked example)

Context: a cron job's `last_delivery_error` read:
"live adapter send failed: Forbidden: bot was kicked from the supergroup chat; ... Telegram send failed: Forbidden: bot was kicked from the supergroup chat"

The user believed it was already fixed. Verification procedure (read-only, no writes):

## 1. Load the bot token from the profile .env

`~/.hermes/profiles/<name>/.env` contains `TELEGRAM_BOT_TOKEN=...`. Read it without echoing secrets:

```python
token = None
with open(".env", "r", encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if line.startswith("TELEGRAM_BOT_TOKEN="):
            token = line.split("=", 1)[1].strip().strip('"').strip("'")
            break
```

## 2. Confirm bot identity

```python
req = urllib.request.Request(f"https://api.telegram.org/bot{token}/getMe")
me = json.loads(urllib.request.urlopen(req, timeout=15).read())
print("BOT:", me.get("result", {}).get("username", "?"))
```

## 3. Probe each chat id with getChat

```python
for cid in ["-1004346387239", "-1003740504045"]:
    req = urllib.request.Request(
        f"https://api.telegram.org/bot{token}/getChat",
        data=urllib.parse.urlencode({"chat_id": cid}).encode())
    chat = json.loads(urllib.request.urlopen(req, timeout=15).read())
    res = chat.get("result", {})
    print(f"{cid}: OK — {res.get('title')} (type={res.get('type')})")
```

## Observed result (Aug 2026)

```
BOT: Nexis_Aria_Nexaris_bot
-1004346387239: OK — Aoi & Shin (type=supergroup)
-1003740504045: OK — Chaos Control (type=supergroup)
```

Both groups reachable → the "kicked" error was stale; the bot had been re-invited.

## Key lesson

The chat referenced in the error (`-1004346387239`, "Aoi & Shin") was NOT the job's current deliver target (`-1003740504045`, "Chaos Control"). Distinguish:
- the chat named in a stale error, vs
- the chat the job ACTUALLY delivers to (check `cronjob list` → `deliver`).

Confirm the real target with the user, then update memory notes to match the authoritative deliver target.
