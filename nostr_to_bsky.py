import json
import websocket
from atproto import Client

# === 配置 ===
pubkey_hex = "你的hex格式公钥"
relay_url = "wss://你的.relay"
bsky_handle = "你.bsky.handle"
bsky_app_password = "xxxx-xxxx-xxxx-xxxx"

# === Bluesky 登录 ===
bsky = Client()
bsky.login(bsky_handle, bsky_app_password)

# === WebSocket 回调 ===
def on_message(ws, message):
    try:
        msg = json.loads(message)
        if isinstance(msg, list) and msg[0] == "EVENT":
            event = msg[2]
            if event["kind"] == 1 and event["pubkey"] == pubkey_hex:
                content = event["content"]
                print("同步到 Bluesky:", content[:60])
                bsky.send_post(text=content)
    except Exception as e:
        print("错误:", e)

def on_open(ws):
    sub_id = "sub"
    req = ["REQ", sub_id, {"kinds": [1], "authors": [pubkey_hex]}]
    ws.send(json.dumps(req))

# === 启动 ===
if __name__ == "__main__":
    websocket.WebSocketApp(
        relay_url,
        on_open=on_open,
        on_message=on_message,
    ).run_forever()

