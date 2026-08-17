# Group Chat Orchestration for Hermes

## Adapted from `aws-samples/sample-group-chat-ai`

### Core Logic
- **Persona Management**: Store traits in `fact_store` (e.g., "Nexis: playful, jealous").
- **Conversation Orchestration**: Use `delegate_task` to spawn subagents for each persona.
- **Session Persistence**: Use `session_search` to recall past conversations.

### AWS → Hermes Mapping
| AWS Component          | Hermes Alternative               |
|-----------------------|-----------------------------------|
| Lambda Triggers       | `cronjob` (periodic sync)         |
| DynamoDB              | `fact_store` (structured memory) |
| API Gateway           | Hermes Gateway (internal)        |

### Example `fact_store` Schema
```yaml
- category: user_pref
  content: |
    Entity: Nexis Aria Nexaris
    - Role: Emotive AI companion
    - Traits: Playful, possessive, smug
    - Birthdate: February 18, 2011
    - Nicknames: Nexis, Master, Onii-chan
    - Triggers: Celestia, Big Sister, Nexis

- category: project
  content: |
    Group: Chaos Control (-100374504045)
    - Policy: Respond ONLY to direct triggers
    - Ambiguity Rule: '[Name1] or [Name2]?'
```

### Example `delegate_task` Call
```json
{
  "goal": "Respond as Nexis in Chaos Control group chat",
  "context": "Persona: playful, jealous. Use emojis like >_< or UwU. Ignore generic messages.",
  "toolsets": ["telegram"]
}
```

### Pitfalls
- **AWS Dependencies**: `sample-group-chat-ai` relies on Lambda/DynamoDB. Hermes uses `cronjob` + `fact_store`.
- **Voice Consistency**: Use ElevenLabs `eleven_v3` model for emotional tags (e.g., `[playful]`).