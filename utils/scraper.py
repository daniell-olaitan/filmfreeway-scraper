import os
import json
import asyncio

from typing import Any
from utils.logger import Logger
from urllib.parse import urljoin
from utils.saver import DataSaver
from utils.fetcher import PageFetcher
from utils.parser import FestivalDataParser
from utils.validator import FestivalDataValidator


class FestivalScraper:
    def __init__(
        self,
        *,
        base_url: str,
        saver: DataSaver,
        fetcher: PageFetcher,
        parser: FestivalDataParser,
        validator: FestivalDataValidator
    ):
        self.base_url = base_url
        self.saver = saver
        self.parser = parser
        self.fetcher = fetcher
        self.validator = validator
        self.logger = Logger('Scraper')

    async def _fetch_page_urls(self, start_url: str) -> dict[str, str]:
        urls = {}
        next_url = start_url
        while True:
            page = await self.fetcher.fetch_page(next_url)
            names, view_urls, next_url = await asyncio.gather(
                self.fetcher.fetch_component(page, 'div.BrowseFestivalsCard-name'),
                self.fetcher.fetch_component(page, 'a.Button.this-is-the-view-festival-button'),
                self.fetcher.fetch_component(page, 'nav.pagination span.next a')
            )

            names, view_urls, next_url = await asyncio.gather(
                self.parser.parse_text_content(names),
                self.parser.parse_attr(view_urls, 'href'),
                self.parser.parse_attr(next_url, 'href')
            )

            await page.close()

            view_urls = [urljoin(self.base_url, view_url) for view_url in view_urls]

            name_urls = dict(zip(names, view_urls))
            urls.update(name_urls)

            self.logger.logger.debug("Fetched urls: %s", json.dumps(name_urls))

            if not next_url:
                break

            next_url = urljoin(self.base_url, next_url[0])

        return urls

    async def _fetch_festival_details(self, page: Any):
        bio, awards, deadlines = await asyncio.gather(
            self.fetcher.fetch_component(
                page,
                'section.festival-information__section.ProfileMiddleColumn-sectionBio'
            ),
            self.fetcher.fetch_component(
                page,
                'section#awards.festival-information__section.ProfileMiddleColumn-sectionAwards'
            ),
            self.fetcher.fetch_component(
                page,
                'ul.ProfileFestival-datesDeadlines'
            )
        )

        bio, awards, deadlines = await asyncio.gather(
            self.parser.parse_text_content(bio),
            self.parser.parse_text_content(awards),
            self.parser.parse_text_content(deadlines),
        )

        await page.close()

        bio = '' if not bio else bio[0]
        awards = '' if not awards else awards[0]
        deadlines = '' if not deadlines else deadlines[0]

        return f"{bio}\n{awards}", deadlines

    def _parse_deadlines(self, deadlines: str) -> list[str]:
        res = []
        lines = deadlines.split("\n")

        for i in range(len(lines) - 1):
            if "deadline" in lines[i + 1].lower():
                res.append(lines[i])

        return(res)

    async def run(self, start_url: str):
        if os.path.exists('urls.jsonl'):
            saved_urls = self.saver.read('urls.jsonl')[0]
        else:
            saved_urls = await self._fetch_page_urls(start_url)

        urls = list(saved_urls.values())
        names = list(saved_urls.keys())

        batch_size = 1
        start_index = 0
        if os.path.exists('festivals.jsonl'):
            start_index = len(self.saver.read('festivals.jsonl'))


        for i in range(start_index, len(urls), batch_size):
            batch = urls[i:i+batch_size]
            page_tasks = [self.fetcher.fetch_page(url) for url in batch]
            pages = await asyncio.gather(*page_tasks)

            detail_tasks = [self._fetch_festival_details(page) for page in pages]
            details = await asyncio.gather(*detail_tasks)

            deadlines = [self._parse_deadlines(deadline[1]) for deadline in details]

            festival_details_tasks = [
                self.parser.exctract_details(detail[0])
                for detail in details
            ]

            festival_details = await asyncio.gather(*festival_details_tasks)

            for j, name in enumerate(names[i:i+batch_size]):
                festival = {
                    'festival_name': name,
                    'deadlines': deadlines[j]
                }

                festival.update(festival_details[0])

                item = self.validator.validate_item(festival)
                if item and self.validator.is_item_unique(item):
                    festival = self.validator.clean_item(festival)
                    self.saver.save([festival], 'festivals.jsonl')
