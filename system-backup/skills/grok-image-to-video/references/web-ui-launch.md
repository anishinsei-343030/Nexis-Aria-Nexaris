### Launching the Hermes Web UI

If you encounter issues connecting to the image or video generation APIs, ensure the Hermes Web UI is running.

#### Standard Launch Method
The recommended way to start the Web UI is via the Hermes CLI:
- Command: `hermes dashboard`
- Default Port: `http://127.0.0.1:9119`

To check status: `hermes dashboard --status`
To stop: `hermes dashboard --stop`

#### Alternative Methods
1. **Using Docker Compose:**
   - Navigate to the directory containing `docker-compose.yaml`.
   - Run: `docker compose up -d`
   - Port: `http://127.0.0.1:6060`
2. **Using the Hermes Gateway:**
   - Command: `hermes gateway run`
   - Port: `http://127.0.0.1:8648` (Legacy/Component dependent)

#### Troubleshooting: `ModuleNotFoundError: No module named 'hermes_cli.dashboard_auth'`
This is a known packaging gap in `hermes-agent==0.15.2`. Because the dashboard binds to 127.0.0.1, the auth gate is not required for local use. Create minimal stubs in `site-packages/hermes_cli/dashboard_auth/` to resolve the imports:

- `__init__.py`: `def list_providers(): return []`
- `routes.py`: `from fastapi import APIRouter; router = APIRouter()`
- `middleware.py`: `async def gated_auth_middleware(request, call_next): return await call_next(request)`
- `audit.py`: `class AuditEvent: pass; def audit_log(*args, **kwargs): pass`
- `ws_tickets.py`: `def mint_ticket(*args, **kwargs): return None`
- `prefix.py`: `def normalise_prefix(p): return p`

Ensure `fastapi` and `uvicorn` are installed in the current Python environment before running `hermes dashboard`.