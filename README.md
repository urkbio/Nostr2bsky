# Nostr2bsky

一个实时将Nostr消息同步到Bluesky的工具。基于事件驱动机制，无需固定轮询时间间隔，可以实时同步你在Nostr上发布的内容到Bluesky。

## 特点

- 事件驱动：通过WebSocket实时监听Nostr relay的事件
- 实时同步：只要relay保持连接，消息就能实时同步
- 轻量运行：无需暴露端口，可在后台静默运行
- 简单配置：只需配置少量参数即可使用

## 依赖

```
atproto
websocket-client
```

## 配置

在 `nostr_to_bsky.py` 中配置以下参数：

```python
pubkey_hex = "你的hex格式公钥"  # Nostr的公钥（hex格式）
relay_url = "wss://你的.relay"   # Nostr的relay地址
bsky_handle = "你.bsky.handle"   # Bluesky的用户名
bsky_app_password = "xxxx-xxxx-xxxx-xxxx"  # Bluesky的App Password
```

## 安装

### 1. 创建并激活虚拟环境

```bash
# 创建虚拟环境
python3 -m venv venv

# 激活虚拟环境
# macOS/Linux
source venv/bin/activate
# Windows
# venv\Scripts\activate
```

### 2. 安装依赖

在虚拟环境激活的状态下，安装所需依赖：

```bash
pip install -r requirements.txt
```

## 运行

确保虚拟环境已激活，然后运行程序：

### 前台运行

```bash
python nostr_to_bsky.py
```

### 后台运行

```bash
nohup python nostr_to_bsky.py > sync.log 2>&1 &
```

后台运行时，日志会被写入到 `sync.log` 文件中。

### 退出虚拟环境

当需要退出虚拟环境时，执行：

```bash
deactivate
```

## 工作原理

1. 程序通过WebSocket连接到指定的Nostr relay
2. 订阅指定公钥的kind 1类型事件（文本消息）
3. 当收到新的事件时，程序会自动将消息内容同步发布到Bluesky
4. 只要relay连接保持，就能持续接收实时事件

## 注意事项

- 请确保你的Bluesky App Password正确且有效
- 确保Nostr的relay地址可以正常访问
- 建议使用稳定的网络环境运行
- 运行程序前确保已激活虚拟环境