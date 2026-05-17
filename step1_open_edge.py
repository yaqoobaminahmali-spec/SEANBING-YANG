import asyncio
import os
import sys
from playwright.async_api import async_playwright


def find_edge():
    """查找 Edge 可执行文件路径（Windows）"""
    candidates = [
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
        os.path.expandvars(r"%LOCALAPPDATA%\Microsoft\Edge\Application\msedge.exe"),
    ]
    for path in candidates:
        if os.path.exists(path):
            return path
    return None


async def main():
    async with async_playwright() as p:
        edge_path = find_edge()

        if edge_path:
            print(f"找到 Edge: {edge_path}")
        else:
            print("未找到 Edge 安装路径，尝试使用 channel 方式启动...")

        try:
            if edge_path:
                browser = await p.chromium.launch(
                    executable_path=edge_path,
                    headless=False,
                )
            else:
                browser = await p.chromium.launch(
                    channel="msedge",
                    headless=False,
                )
            print("Microsoft Edge 已成功打开！")
        except Exception as e:
            print(f"启动 Edge 失败: {e}")
            print("提示：请在终端运行以下命令安装 Edge 驱动后重试：")
            print("  playwright install msedge")
            sys.exit(1)

        context = await browser.new_context()
        page = await context.new_page()
        print("浏览器就绪，等待 10 秒后关闭...")
        await asyncio.sleep(10)
        await browser.close()
        print("完成")


asyncio.run(main())
