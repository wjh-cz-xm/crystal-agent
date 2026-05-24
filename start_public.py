"""晶体智能助手 — 公网启动（FastAPI + ngrok）"""
import io, os, re, signal, subprocess, sys, time, threading
from pathlib import Path

PROJECT = Path(__file__).parent
NGROK = PROJECT / "ngrok.exe"

# UTF-8 输出
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")


def start_server():
    """启动 FastAPI 服务"""
    import uvicorn
    sys.path.insert(0, str(PROJECT / "backend"))
    from config import HOST, PORT
    print(f"[server] 启动 http://{HOST}:{PORT}")
    uvicorn.run("backend.main:app", host=HOST, port=PORT, log_level="warning")


def start_ngrok():
    """启动 ngrok 隧道"""
    if not NGROK.exists():
        print("[ngrok] ngrok.exe 不存在，跳过")
        return

    # 清除代理环境变量，ngrok 免费版不支持走代理
    env = os.environ.copy()
    for k in ["HTTP_PROXY", "HTTPS_PROXY", "http_proxy", "https_proxy", "all_proxy"]:
        env.pop(k, None)

    proc = subprocess.Popen(
        [str(NGROK), "http", "8000", "--log=stdout"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        encoding="utf-8",
        errors="replace",
        env=env,
    )

    # 等待 ngrok 启动并提取公网 URL
    url = None
    for line in proc.stdout:
        print(f"[ngrok] {line.rstrip()}")
        if not url:
            m = re.search(r"url=(https://[^\s]+)", line)
            if m:
                url = m.group(1)
                print(f"\n{'='*60}")
                print(f"  公网地址: {url}")
                print(f"  分享此链接即可访问晶体智能助手")
                print(f"{'='*60}\n")
                break
        time.sleep(0.05)

    # 持续读取 ngrok 日志
    try:
        for line in proc.stdout:
            pass
    except KeyboardInterrupt:
        pass
    finally:
        proc.terminate()


def main():
    print("=" * 60)
    print("  晶体智能助手 — 公网模式")
    print("=" * 60)

    server_thread = threading.Thread(target=start_server, daemon=True)
    server_thread.start()

    # 等服务器就绪
    time.sleep(2)

    try:
        start_ngrok()
    except KeyboardInterrupt:
        print("\n[shutdown] 服务已停止")


if __name__ == "__main__":
    main()
