---\nname: free-model-constraints\ndescription: name: free-model-constraints\nversion: 1.0.0\nplatforms: [linux, macos, windows]\n---
name: free-model-constraints
description: Enforce constraints for free models via 9router (Gemini, Groq, Cerebras, Mistral). Use this skill to guide tool usage and validate outputs.
version: 1.0.0
platforms: [linux, macos, windows]
---

# Free Model Constraints for 9router

## Tool Boundaries
- **Protected files**: Never use `patch` on `.env`, `config.yaml`, or `skills/`.
- **TTS limits**: Free models enforce strict character limits (e.g., OpenAI: 4096 chars). Truncate input if needed.
- **API timeouts**: 30s. Retry once with exponential backoff.
- **Rate limits**: 5 requests/minute. Batch tool calls where possible.

## Output Validation
- **TTS**: Verify length and provider-specific caps.
- **Patch**: Confirm file syntax (YAML/JSON linting).
- **Skill management**: Validate skill file changes.

## Fallbacks
- If a tool fails, suggest alternatives (e.g., `write_file` for unprotected files).
- Use simpler tools (e.g., `terminal` over `browser` for free models).
