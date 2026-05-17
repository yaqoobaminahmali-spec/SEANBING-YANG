import asyncio
from playwright.async_api import async_playwright

LOGIN_URL = "https://dcrauth.antonoil.com/login?service=https%3A%2F%2Fdcr.antonoil.com%2Flogin%2Fcas#/uploadNew/MyUploadListNew"
USERNAME = "杨小兵"
PASSWORD = "2020203@YLYR"


async def login(page):
    print("正在打开经营辅助系统登录页面...")
    await page.goto(LOGIN_URL, timeout=30000)
    await page.wait_for_load_state("networkidle")
    await asyncio.sleep(3)
    print("页面标题:", await page.title())

    # 如果用户名未预选，尝试填写用户名
    username_selectors = [
        'input[name="username"]',
        'input[placeholder*="用户名"]',
        'input[placeholder*="账号"]',
        'input[type="text"]:first-of-type',
    ]
    for sel in username_selectors:
        try:
            el = await page.query_selector(sel)
            if el:
                val = await el.input_value()
                if not val:
                    await el.fill(USERNAME)
                    print(f"用户名已填入: {USERNAME}")
                else:
                    print(f"用户名已预填: {val}")
                break
        except Exception:
            continue

    # 填写密码
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
        return False

    await asyncio.sleep(1)

    # 点击登录按钮
    login_selectors = [
        'button:has-text("登录")',
        'button[type="submit"]',
        'input[type="submit"]',
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
        await page.keyboard.press("Enter")
        print("已按回车键提交登录")

    await page.wait_for_load_state("networkidle")
    await asyncio.sleep(3)
    print("登录后 URL:", page.url)
    print("登录后标题:", await page.title())
    return True


async def navigate_to_upload(page):
    """导航到填报数据页面"""
    current_url = page.url
    if "uploadNew" not in current_url:
        print("正在导航到填报数据页面...")
        await page.goto(
            "https://dcr.antonoil.com/login/cas#/uploadNew/MyUploadListNew",
            timeout=30000,
        )
        await page.wait_for_load_state("networkidle")
        await asyncio.sleep(3)

    print("当前页面:", await page.title())
    await page.screenshot(path="screenshot_upload_page.png")
    print("截图已保存: screenshot_upload_page.png")


async def fill_data(page):
    """在填报页面填写数据"""
    print("开始填报数据...")
    await asyncio.sleep(2)

    # 点击"新增"按钮（如有）
    new_btn_selectors = [
        'button:has-text("新增")',
        'button:has-text("添加")',
        'button:has-text("上传")',
        '.el-button:has-text("新增")',
    ]
    for sel in new_btn_selectors:
        try:
            el = await page.query_selector(sel)
            if el:
                await el.click()
                print(f"已点击新增按钮: {sel}")
                await asyncio.sleep(2)
                break
        except Exception:
            continue

    await page.screenshot(path="screenshot_fill_form.png")
    print("填报页面截图已保存: screenshot_fill_form.png")
    print("请根据实际表单字段补充填报逻辑")


async def main():
    async with async_playwright() as p:
        # 优先使用 Microsoft Edge，不可用时回退到 Chromium
        try:
            browser = await p.chromium.launch(
                channel="msedge",
                headless=False,
            )
            print("已启动 Microsoft Edge 浏览器")
        except Exception:
            print("Edge 不可用，使用 Chromium 替代")
            browser = await p.chromium.launch(headless=False)

        context = await browser.new_context(ignore_https_errors=True)
        page = await context.new_page()

        try:
            success = await login(page)
            if not success:
                print("登录失败，退出")
                await browser.close()
                return

            await navigate_to_upload(page)
            await fill_data(page)

            print("流程完成，浏览器将保持打开 30 秒...")
            await asyncio.sleep(30)
        except Exception as e:
            print(f"发生错误: {e}")
            await page.screenshot(path="screenshot_error.png")
        finally:
            await browser.close()


asyncio.run(main())
