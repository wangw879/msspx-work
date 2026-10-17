#!/usr/bin/env python3
"""打印当前机器的系统信息，用于在 GitHub Actions runner 中验证执行环境。

仅依赖 Python 标准库，避免在 runner 上安装第三方包。
输出为纯文本，便于直接在 Actions 日志中查看。
"""
import getpass
import os
import platform
import socket
import sys
import uuid


def outbound_ip() -> str:
    """探测本机对外通信使用的出口 IP（UDP connect，不实际发送数据）。"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        sock.connect(("8.8.8.8", 80))
        return sock.getsockname()[0]
    except OSError:
        return "unknown"
    finally:
        sock.close()


def mem_summary() -> str:
    """从 /proc/meminfo 读取总/可用内存，返回可读字符串。"""
    try:
        with open("/proc/meminfo", encoding="utf-8") as f:
            info = {line.split(":")[0]: line.split()[1] for line in f if ":" in line}
        total = int(info.get("MemTotal", 0)) // 1024
        avail = int(info.get("MemAvailable", 0)) // 1024
        return f"{total} MB / {avail} MB"
    except (OSError, ValueError):
        return "unknown"


def section(title: str) -> None:
    """打印带分隔线的区块标题。"""
    print("=" * 60)
    print(title)
    print("=" * 60)


def main() -> None:
    section("主机信息")
    print(f"主机名        : {socket.gethostname()}")
    print(f"当前用户      : {getpass.getuser()}")
    print(f"UID           : {os.getuid()}")
    print(f"系统平台      : {platform.platform()}")
    print(f"内核版本      : {platform.release()}")
    print(f"系统类型      : {platform.system()}")

    section("硬件资源")
    print(f"CPU 架构      : {platform.machine()}")
    print(f"CPU 型号      : {platform.processor() or 'unknown'}")
    print(f"CPU 核心数    : {os.cpu_count()}")
    print(f"内存(总/可用) : {mem_summary()}")

    section("网络标识")
    print(f"出口 IP       : {outbound_ip()}")
    print(f"MAC 派生 ID   : {uuid.uuid1().hex[:16]}")

    section("运行时")
    print(f"Python 版本   : {sys.version.split()[0]}")
    print(f"可执行文件    : {sys.executable}")
    print(f"工作目录      : {os.getcwd()}")
    print(f"进程 PID      : {os.getpid()}")

    section("GitHub Actions 上下文")
    # 仅在这些变量存在时打印，便于区分本地执行与 runner 执行
    gh_keys = (
        "CI",
        "GITHUB_REPOSITORY",
        "GITHUB_RUN_ID",
        "GITHUB_RUN_NUMBER",
        "GITHUB_WORKFLOW",
        "RUNNER_ARCH",
        "RUNNER_NAME",
        "RUNNER_OS",
    )
    found = False
    for key in sorted(gh_keys):
        value = os.environ.get(key)
        if value is not None:
            print(f"{key:<16}: {value}")
            found = True
    if not found:
        print("（未检测到 GitHub Actions 环境变量，当前应为本地执行）")


if __name__ == "__main__":
    main()
