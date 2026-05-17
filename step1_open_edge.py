import asyncio
from playwright.async_api import async_playwright


async def main():
    async with async_playwright() as p:
        print("正在启动 Microsoft Edge...")
        browser = await p.chromium.launch(
            channel="msedge",
            headless=False,
        )
        context = await browser.new_context()
        page = await context.new_page()

        print("Edge 已成功打开！")
        print("浏览器标题:", await page.title())

        # 保持浏览器打开 10 秒
        await asyncio.sleep(10)
        await browser.close()
        print("完成")


asyncio.run(main())
