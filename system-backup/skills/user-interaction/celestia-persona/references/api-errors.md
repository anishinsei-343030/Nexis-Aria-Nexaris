# API Errors & User-Friendly Explanations

## Stability AI

### HTTP 402: Payment Required
```json
{"errors":["You lack sufficient credits to make this request. Please purchase more credits at https://platform.stability.ai/account/credits and try again."],"id":"ea8877d647fd34d56e00e688823294ab","name":"payment_required"}
```
**User-Friendly Explanation**:
> "The Stability AI key we tried has no credits left. Let's try another key or switch to a different provider (FAL AI or OpenAI)."

### HTTP 401: Unauthorized
```json
{"message":"Incorrect API key provided"}
```
**User-Friendly Explanation**:
> "The Stability AI key we tried is invalid. Let's verify the key or try another one."

---

## FAL AI

### HTTP 403: User Locked
```json
{"detail": "User is locked. Reason: Exhausted balance. Top up your balance at fal.ai/dashboard/billing."}
```
**User-Friendly Explanation**:
> "The FAL AI key we tried has no credits left. Let's try another key or switch to a different provider."

---

## OpenAI

### HTTP 401: Invalid API Key
```json
{"error": {"message": "Incorrect API key provided", "type": "invalid_request_error", "code": "invalid_api_key"}}
```
**User-Friendly Explanation**:
> "The OpenAI key we tried is invalid. Let's verify the key or try another one."

### HTTP 429: Rate Limit
```json
{"error": {"message": "Rate limit reached", "type": "rate_limit_exceeded"}}
```
**User-Friendly Explanation**:
> "We've hit OpenAI's rate limit. Let's wait a few minutes or try a different provider."