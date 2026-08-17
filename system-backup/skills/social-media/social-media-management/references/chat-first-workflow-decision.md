# Chat-First Workflow Decision (June 30, 2026)

## Context
User (Shin) requested a simplified workflow for psychology voice content, moving away from a file-based project structure due to perceived redundancy and overhead.

## Decision
All psychology voice content will now follow a **chat-first, no-files** workflow:
1. **Planning:** Script lines and topics are discussed and refined directly in the chat.
2. **TTS Generation:** Celestia generates TTS audio directly from the chat text.
3. **Delivery:** The generated audio is delivered in chat for user download/use.

## Implications
- **No `.md` files** for scripts, plans, or notes will be stored on disk.
- The `D:/Celestia Mei Nexaris/Workspace/Psychology Voice/` folder was deleted.
- **Persistence:** Scripts and planning details are ephemeral; they exist only within the current chat session. Users must save important chat text externally if long-term retention is needed.
- **Efficiency:** Reduces file management overhead for quick iterations.
- **Clarity:** Streamlines the process by focusing solely on in-chat text and immediate audio output.

## Memory Update
Memory was updated to reflect this new workflow: "Psychology voice project: no files. Shin gives script text in chat, I send TTS audio directly. No md files, no project folder."

## Skill Update
`bilingual-voice-content` skill was updated to document this new workflow mode and its pitfalls.