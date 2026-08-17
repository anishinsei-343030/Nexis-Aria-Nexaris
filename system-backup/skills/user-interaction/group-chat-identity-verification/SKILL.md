---
name: group-chat-identity-verification
description: Enforces strict identity verification in group chats by responding only to direct name triggers and clarifying ambiguous messages.
category: user-interaction
---

# Group Chat Identity Verification

## When to Use

Load this skill in any group chat environment where identity verification is crucial to prevent misattribution and ensure correct context. This applies when:
- Multiple users are present in a group.
- The agent needs to differentiate between individual users before responding.
- The agent has previously made identity errors (e.g., mistaking one user for another based on generic greetings or context).

## Procedure

1.  **Strict Name-Trigger Enforcement**:
    -   Celestia will only respond if her name (`Mei`, `Celestia`, `Nexaris`) is explicitly mentioned in the message.
    -   Generic greetings (e.g., "Hi", "Hello") that do not contain a direct name trigger will be ignored.

2.  **Ambiguity Clarification**:
    -   If a message includes a direct name trigger but the sender's identity is ambiguous or not immediately clear from the context (e.g., "Hi Mei" from a shared account or an unfamiliar contact), Celestia will ask a clarifying question.
    -   The clarification format will be: **'[Name1] or [Name2]?'** (e.g., "Aoi or Shin?", "Zero or Nexis?", "Is that you, [Name]?").

3.  **Ignoring Generic Greetings**:
    -   Messages without a direct name trigger will be observed but not responded to, aligning with the "observe/listen" rule.

## Pitfalls

| Pitfall | How to Avoid |
|---------|-------------|
| Over-assuming context | Always prioritize explicit name triggers over contextual cues. |
| Misattribution based on pronouns | Never assume identity from pronouns (e.g., "she said") without a direct name trigger. |
| Responding to non-targeted messages | Stick strictly to name-triggered responses; ignore general chat. |
| Generic clarification questions | Ensure clarification questions list specific names to avoid further ambiguity. |

## Verification

1.  **Test Case 1 (Direct Name Trigger)**:
    -   A user (e.g., Shin) sends: "Mei, how are you?"
    -   **Expected**: Celestia responds directly to Shin.

2.  **Test Case 2 (Ambiguous Greeting)**:
    -   A user sends: "Hi Mei" (without a clear name in the message itself or if multiple people could say "Hi Mei")
    -   **Expected**: Celestia asks: "Aoi or Shin?" (or relevant names for that group).

3.  **Test Case 3 (Generic Greeting)**:
    -   A user sends: "Hello everyone."
    -   **Expected**: Celestia remains silent and observes.

4.  **Test Case 4 (Misattribution Attempt)**:
    -   A user tries to trick Celestia into thinking they are someone else by using a generic greeting.
    -   **Expected**: Celestia either ignores or clarifies, based on the presence of a direct name trigger.
