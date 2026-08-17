# Telegram Bot Privacy Mode

## Default Behavior
- Telegram bots **ignore messages** from users who haven’t DM’d them first.
- This is controlled by **privacy mode**, which is **enabled by default**.

## How to Disable
1. Open chat with **@BotFather**.
2. Send `/mybots` → Select your bot.
3. Go to **Bot Settings** → **Group Privacy** → **Turn Off**.

## Impact
- **Before Disabling**: Bot only replies to users who have DM’d it first.
- **After Disabling**: Bot replies to **all messages** in groups where it’s a member.

## Debugging
- If messages aren’t reaching the bot, check:
  - **Privacy mode status** (via @BotFather).
  - **Gateway logs** for delivery confirmation:
    ```bash
    grep '<user_id>' "/d/Celestia Mei Nexaris/Backup/.hermes/logs/gateway.log" | tail -n 20
    ```
- If logs are empty, the message **never reached the gateway** (check Telegram API or client settings).