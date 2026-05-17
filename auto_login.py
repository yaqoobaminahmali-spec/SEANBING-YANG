import asyncio
from playwright.async_api import async_playwright

URL = "https://dcrauth.antonoil.com/login?service=https%3A%2F%2Fdcr.antonoil.com%2Flogin%2Fcas#/uploadNew/MyUploadListNew"
USERNAME = "yangxiaobing"
PASSWORD = "2020203@YLYR"

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            executable_path="/opt/pw-browsers/chromium-1194/chrome-linux/chrome"
        )
        context = await browser.new_context(ignore_https_errors=True)
        page = await context.new_page()

        print(f"正在打开页面: {URL}")
        await page.goto(URL, timeout=30000)
        await page.wait_for_load_state("networkidle")
        await asyncio.sleep(5)  # 等待 JS 渲染完成

        print("页面标题:", await page.title())
        print("当前URL:", page.url)

        # 截图查看页面结构
        await page.screenshot(path="screenshot_before_login.png")
        print("截图已保存: screenshot_before_login.png")

        # 打印页面中所有 input 元素
        inputs = await page.query_selector_all("input")
        print(f"找到 {len(inputs)} 个输入框:")
        for i, inp in enumerate(inputs):
            name = await inp.get_attribute("name")
            type_ = await inp.get_attribute("type")
            placeholder = await inp.get_attribute("placeholder")
            print(f"  [{i}] name={name}, type={type_}, placeholder={placeholder}")

        # 尝试填写用户名和密码
        username_selectors = ['input[name="username"]', 'input[type="text"]', 'input#username', 'input[placeholder*="用户"]', 'input[placeholder*="账号"]']
        password_selectors = ['input[name="password"]', 'input[type="password"]', 'input#password']

        username_filled = False
        for sel in username_selectors:
            try:
                el = await page.query_selector(sel)
                if el:
                    await el.fill(USERNAME)
                    print(f"用户名已填入，使用选择器: {sel}")
                    username_filled = True
                    break
            except Exception:
                continue

        password_filled = False
        for sel in password_selectors:
            try:
                el = await page.query_selector(sel)
                if el:
                    await el.fill(PASSWORD)
                    print(f"密码已填入，使用选择器: {sel}")
                    password_filled = True
                    break
            except Exception:
                continue

        if username_filled and password_filled:
            # 尝试点击登录按钮
            submit_selectors = ['button[type="submit"]', 'input[type="submit"]', 'button:has-text("登录")', 'button:has-text("Login")', '.login-btn', '#loginBtn']
            for sel in submit_selectors:
                try:
                    el = await page.query_selector(sel)
                    if el:
                        await el.click()
                        print(f"已点击登录按钮，使用选择器: {sel}")
                        break
                except Exception:
                    continue

            await page.wait_for_load_state("networkidle")
            await asyncio.sleep(3)

            print("登录后页面标题:", await page.title())
            print("登录后页面URL:", page.url)
            await page.screenshot(path="screenshot_after_login.png")
            print("截图已保存: screenshot_after_login.png")
        else:
            print("未能找到用户名或密码输入框，请查看截图确认页面结构")

        await browser.close()

asyncio.run(main())
