import asyncio
from playwright.async_api import async_playwright

URL = "https://dcrauth.antonoil.com/login?service=https%3A%2F%2Fdcr.antonoil.com%2Flogin%2Fcas#/uploadNew/MyUploadListNew"
PASSWORD = "2020203@YLYR"

async def main():
    async with async_playwright() as p:
        # 使用 Microsoft Edge 浏览器
        browser = await p.chromium.launch(
            channel="msedge",       # 指定使用 Edge
            headless=False,         # False = 显示浏览器窗口
        )
        context = await browser.new_context(ignore_https_errors=True)
        page = await context.new_page()

        print("正在打开登录页面...")
        await page.goto(URL, timeout=30000)
        await page.wait_for_load_state("networkidle")
        await asyncio.sleep(3)

        print("页面标题:", await page.title())

        # 页面已预选用户"杨小兵"，只需填写密码
        # 尝试多种密码框选择器
        password_selectors = [
            'input[type="password"]',
            'input[name="password"]',
            'input[placeholder*="密码"]',
            'input[placeholder*="Password"]',
        ]

        password_filled = False
        for sel in password_selectors:
            try:
                el = await page.wait_for_selector(sel, timeout=5000)
                if el:
                    await el.click()
                    await el.fill(PASSWORD)
                    print(f"密码已填入，选择器: {sel}")
                    password_filled = True
                    break
            except Exception:
                continue

        if not password_filled:
            print("未找到密码框，截图保存以供检查")
            await page.screenshot(path="screenshot_debug.png")
            await browser.close()
            return

        await asyncio.sleep(1)

        # 点击"登录"按钮
        login_selectors = [
            'button:has-text("登录")',
            'input[type="submit"]',
            'button[type="submit"]',
            '.login-btn',
            'button:has-text("Login")',
        ]

        login_clicked = False
        for sel in login_selectors:
            try:
                el = await page.query_selector(sel)
                if el:
                    await el.click()
                    print(f"已点击登录按钮，选择器: {sel}")
                    login_clicked = True
                    break
            except Exception:
                continue

        if not login_clicked:
            # 尝试按回车键提交
            await page.keyboard.press("Enter")
            print("已按回车键提交")

        await page.wait_for_load_state("networkidle")
        await asyncio.sleep(3)

        print("登录后URL:", page.url)
        print("登录后标题:", await page.title())

        # 保持浏览器打开30秒
        await asyncio.sleep(30)
        await browser.close()

asyncio.run(main())
