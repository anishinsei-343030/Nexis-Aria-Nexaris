This file documents specific instances of identity misattribution in group chats, which led to the development of the 'Group Chat Identity Verification' policy within the `user-interaction` skill.

**Incident 1: Aoi/Shin Misattribution (June 16, 2026)**
- **Context**: In the 'Aoi & Shin' Telegram group, Aoi messaged 'Hi Mei'.
- **Celestia's Response (prior to policy update)**: 'Hello there, Shin! It's wonderful to hear from you.'
- **User Correction**: Aoi clarified, 'This is Aoi thought'. Shin then requested the policy update.
- **Learning**: Initial response mechanism relied too heavily on group context and general greeting patterns, leading to misattribution. Lack of explicit identity confirmation was the root cause.

**Resolution**: Implemented strict name-trigger policy and explicit clarification questions when identity is ambiguous, as detailed in the `user-interaction` skill.