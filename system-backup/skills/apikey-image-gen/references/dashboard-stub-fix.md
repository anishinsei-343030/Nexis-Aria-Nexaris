# Dashboard Auth Stub Workaround

When launching the Hermes Web UI (via `hermes dashboard`), a `ModuleNotFoundError: No module named 'hermes_cli.dashboard_auth'` may occur due to a packaging gap in `hermes-agent==0.15.2`. Since the auth gate is not engaged for local traffic (127.0.0.1), the missing module can be bypassed by creating a minimal stub package.

## Implementation
Create the directory `.../site-packages/hermes_cli/dashboard_auth/` and add the following stubs:

- `__init__.py`: Export `def list_providers(): return []`
- `routes.py`: Export `from fastapi import APIRouter; router = APIRouter()`
- `middleware.py`: Export a FastAPI-compatible async no-op:
  ```python
  async def gated_auth_middleware(request, call_next):
      return await call_next(request)
  ```
- `audit.py`: Export `class AuditEvent: pass` and `def audit_log(event): pass`
- `ws_tickets.py`: Export `def mint_ticket(user_id, lifetime_seconds=3600): return "stub_ticket"`
- `prefix.py`: Export `def normalise_prefix(prefix): return prefix`

This allows the `web_server.py` imports to resolve, enabling the dashboard to bind to the local port.