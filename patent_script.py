import asyncio
from pyppeteer import launch
import tkinter
import Sensitive


class Patent():
    def __init__(self):
        tk = tkinter.Tk()
        width = tk.winfo_screenwidth()
        height = tk.winfo_screenheight()
        tk.quit()

        browser = await launch(headless=False,
                               args=[f'--window-size={width},{height}'],
                               ignoreDefaultArgs="enable-automation")
        self.page = await browser.newPage()
        await self.page.setViewport(viewport={'width': width, 'height': height})

    async def login(self):
        await self.page.goto('http://cpquery.cnipa.gov.cn/')
        await self.page.evaluate(
            '''() =>{ Object.defineProperties(navigator,{ webdriver:{ get: () => false } }) }''')
        # await page.evaluate('''() =>{ window.navigator.chrome = { runtime: {},  }; }''')
        await self.page.waitForSelector("#publiclogin")
        await asyncio.sleep(2)
        username = await self.page.waitForSelector("#username1")
        await username.type(Sensitive.account_text)
        password = await self.page.waitForSelector("#password1")
        await password.type(Sensitive.password_text)
        wait = input("authentication-done:")
        login = await self.page.waitForSelector("#publiclogin")
        await login.click()
        await asyncio.sleep(2)
        agree = await self.page.waitForSelector("#agreeid")
        await agree.click()
        await asyncio.sleep(0.5)
        go_btn = await self.page.waitForSelector("#goBtn")
        await go_btn.click()

    async def search(self, company=""):
        if company == "":
            company = "江苏民威电碳科技有限公司"
        applicant = await self.page.waitForSelector('#select-key\:shenqingrxm')
        await applicant.type(company)

    async def run(self):
        await self.login()


def main():
    pt = Patent()
    asyncio.get_event_loop().run_until_complete(pt.run())
    asyncio.get_event_loop().run_forever()


if __name__ == '__main__':
    main()
