import asyncio
from playwright.async_api import async_playwright

URL = "https://dcrauth.antonoil.com/login?service=https%3A%2F%2Fdcr.antonoil.com%2Flogin%2Fcas#/uploadNew/MyUploadListNew"

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            executable_path="/opt/pw-browsers/chromium-1194/chrome-linux/chrome"
        )
        context = await browser.new_context(ignore_https_errors=True)
        page = await context.new_page()

        # 监听控制台输出
        page.on("console", lambda msg: print(f"[console] {msg.type}: {msg.text}"))
        page.on("pageerror", lambda err: print(f"[pageerror] {err}"))

        print("打开页面...")
        response = await page.goto(URL, timeout=30000, wait_until="domcontentloaded")
        print(f"HTTP状态码: {response.status if response else 'N/A'}")

        await asyncio.sleep(8)

        content = await page.content()
        print(f"页面HTML长度: {len(content)}")
        print("--- HTML前1000字符 ---")
        print(content[:1000])

        await browser.close()

asyncio.run(main())
