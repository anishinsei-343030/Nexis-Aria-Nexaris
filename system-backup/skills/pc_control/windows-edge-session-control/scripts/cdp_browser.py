#!/usr/bin/env python3
"""
CDP Browser Control — Chrome DevTools Protocol via WebSocket.

Usage:
  python scripts/cdp_browser.py <port> navigate <url>
  python scripts/cdp_browser.py <port> extract html
  python scripts/cdp_browser.py <port> extract links
  python scripts/cdp_browser.py <port> extract json <js-expression>
  python scripts/cdp_browser.py <port> screenshot <output.png>
  python scripts/cdp_browser.py <port> scroll
"""

import sys
import json
import base64
import requests
import websocket


def find_tab(port, url_filter=None):
    resp = requests.get(f"http://127.0.0.1:{port}/json")
    tabs = resp.json()
    if url_filter:
        for t in tabs:
            if url_filter in t.get("url", ""):
                return t
    return tabs[0] if tabs else None


def send(ws, method, params=None, msg_id=1):
    payload = {"id": msg_id, "method": method}
    if params:
        payload["params"] = params
    ws.send(json.dumps(payload))
    resp = ws.recv()
    return json.loads(resp)


def main():
    args = sys.argv[1:]
    if len(args) < 2:
        print("Usage: see script header", file=sys.stderr)
        sys.exit(1)

    port = args[0]
    action = args[1]
    url_filter = args[2] if len(args) > 2 and not args[2].startswith("http") and action == "navigate" else None

    tab = find_tab(port, url_filter)
    if not tab:
        print("No tab found", file=sys.stderr)
        sys.exit(1)

    ws_url = tab["webSocketDebuggerUrl"]
    ws = websocket.create_connection(ws_url)

    if action == "navigate":
        target_url = args[2] if len(args) > 2 else tab["url"]
        send(ws, "Page.enable")
        result = send(ws, "Page.navigate", {"url": target_url})
        print(json.dumps(result, indent=2))

    elif action == "extract":
        sub = args[2] if len(args) > 2 else "html"
        if sub == "html":
            result = send(ws, "Runtime.evaluate", {
                "expression": "document.documentElement.outerHTML"
            })
            print(result["result"]["result"]["value"])
        elif sub == "links":
            result = send(ws, "Runtime.evaluate", {
                "expression": "JSON.stringify(Array.from(document.querySelectorAll('a')).map(a => ({text: a.innerText.trim().substring(0,100), href: a.href})).filter(x => x.text.length > 5))"
            })
            links = json.loads(result["result"]["result"]["value"])
            print(json.dumps(links, indent=2))
        elif sub == "text":
            result = send(ws, "Runtime.evaluate", {
                "expression": "document.body.innerText"
            })
            print(result["result"]["result"]["value"])
        elif sub == "json":
            expr = args[3] if len(args) > 3 else "document.title"
            result = send(ws, "Runtime.evaluate", {"expression": expr})
            print(result["result"]["result"]["value"])

    elif action == "screenshot":
        result = send(ws, "Page.captureScreenshot", {"format": "png"})
        out_path = args[2] if len(args) > 2 else f"screenshot_{port}.png"
        with open(out_path, "wb") as f:
            f.write(base64.b64decode(result["result"]["data"]))
        print(f"Screenshot saved to {out_path}")

    elif action == "scroll":
        result = send(ws, "Runtime.evaluate", {
            "expression": "window.scrollTo(0, document.body.scrollHeight); window.scrollY"
        })
        print(f"Scrolled to y={result['result']['result']['value']}")

    ws.close()


if __name__ == "__main__":
    main()
