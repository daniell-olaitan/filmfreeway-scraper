from utils.logger import Logger
from playwright.async_api import (
    Page,
    Browser,
    Locator,
    Playwright,
    BrowserType
)


class PageFetcher:
    def __init__(self, max_retries: int = 3):
        self.max_retries = max_retries
        self.logger = Logger('Fetcher')
        self.browser: Browser = None

    async def close(self):
        if self.browser:
            await self.browser.close()

    @classmethod
    async def start_browser(
        cls: 'PageFetcher',
        playwright: Playwright,
        browser_type: str,
        max_retries: int = 3
    ) -> 'PageFetcher':
        browser_type: BrowserType = getattr(playwright, browser_type)
        browser = await browser_type.launch(headless=False)

        fetcher = cls(max_retries)
        fetcher.browser = browser

        return fetcher

    async def fetch_page(self, url: str) -> Page:
        self.logger.logger.debug("Fectching page at: %s\n", url)
        while True:
            try:
                page: Page = await self.browser.new_page()
                await page.goto(url, timeout=30000)
                await page.wait_for_load_state('domcontentloaded', timeout=30000)
                if await page.title() == 'Just a moment...':
                    await page.goto(url.rsplit('/', 1)[0], timeout=30000)
                    await page.wait_for_load_state('domcontentloaded', timeout=30000)

                    await page.close()
                    continue

                break
            except Exception as e:
                self.logger.logger.debug("Error: %s", e)
                self.logger.logger.debug("Retrying to fetch page at: %s\n", url)
                await page.close()

        return page

    async def fetch_component(self, page: Page, selector: str) -> Locator:
        return page.locator(selector)
