import json
import re
import websocket
from atproto import Client
from urllib.parse import urlparse

# === 配置 ===
pubkey_hex = "你的hex格式公钥"
relay_url = "wss://你的.relay"
bsky_handle = "你.bsky.handle"
bsky_app_password = "xxxx-xxxx-xxxx-xxxx"

# === Bluesky 登录 ===
bsky = Client()
bsky.login(bsky_handle, bsky_app_password)

def truncate_text(text, max_length=300):
    """截断文本，确保不超过Bluesky的字符限制"""
    if len(text) <= max_length:
        return text
    # 在最后添加省略号
    return text[:max_length-1] + '…'

def process_content(content):
    # 处理标签：将 #tag 转换为 Bluesky 格式
    content = re.sub(r'#(\w+)', r'#\1', content)
    
    # 处理图片链接
    words = content.split()
    images = []
    new_words = []
    
    for word in words:
        # 检查是否是图片URL
        if is_image_url(word):
            try:
                # 使用外部链接
                images.append({
                    'alt': 'Image from Nostr',
                    'image': {
                        '$type': 'app.bsky.embed.external',
                        'external': {
                            'uri': word,
                            'title': 'Nostr Image',
                            'description': 'Image shared from Nostr'
                        }
                    }
                })
                continue  # 跳过URL，不添加到文本内容中
            except Exception as e:
                print(f"处理图片链接失败: {e}")
        new_words.append(word)
    
    # 重建文本内容，不包含图片URL
    new_content = ' '.join(new_words)
    
    # 确保文本长度不超过限制
    new_content = truncate_text(new_content)
    
    return new_content, images

def is_image_url(url):
    """检查URL是否是图片链接"""
    try:
        parsed = urlparse(url)
        path = parsed.path.lower()
        return path.endswith(('.png', '.jpg', '.jpeg', '.gif', '.webp'))
    except:
        return False

# === WebSocket 回调 ===
def on_message(ws, message):
    try:
        msg = json.loads(message)
        if isinstance(msg, list) and msg[0] == "EVENT":
            event = msg[2]
            if event["kind"] == 1 and event["pubkey"] == pubkey_hex:
                content = event["content"]
                print("处理内容:", content[:60])
                
                # 处理内容和图片
                processed_content, images = process_content(content)
                
                # 发送到Bluesky
                if images:
                    # 如果有图片，使用正确的embed格式
                    embed = {
                        '$type': 'app.bsky.embed.external',
                        'external': {
                            'uri': images[0]['image']['external']['uri'],
                            'title': 'Nostr Image',
                            'description': 'Image shared from Nostr'
                        }
                    }
                    bsky.send_post(text=processed_content, embed=embed)
                else:
                    # 如果没有图片，只发送文本
                    bsky.send_post(text=processed_content)
                
                print("发送成功，内容长度:", len(processed_content))
                
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

