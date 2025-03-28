import asyncio
import argparse

from decouple import config
from utils.logger import Logger
from utils.saver import DataSaver
from utils.fetcher import PageFetcher
from utils.scraper import FestivalScraper
from utils.parser import FestivalDataParser
from utils.validator import FestivalDataValidator
from playwright.async_api import async_playwright
from utils.data_models import PROMPT, FestivalItem

BASE_URL = 'https://filmfreeway.com'
START_URL = "https://filmfreeway.com/festivals?utf8=%E2%9C%93&config%5B%5D=entry_fees&config%5B%5D=years_running&config%5B%5D=runtime&config%5B%5D=submit&has_query=&ga_search_category=Festival&q=&call_for_entries=1&ft_gold=0&ft_gold=1&ft_ff=0&ft_ff=1&ft_sc=0&ft_audio=0&ft_photo=0&ft_oe=0&project_category%5B%5D=5&fees=0%3B100&years=1%3B20&runtime=Any&inside_or_outside_country=0&countries=&completion_date=&entry_deadline_when=0&entry_deadline=&event_date_when=0&event_date=&sort=years"


async def main():
    async with async_playwright() as playwright:
        fetcher = await PageFetcher.start_browser(
            playwright=playwright,
            browser_type='chromium'
        )

        saver = DataSaver()
        validator = FestivalDataValidator(FestivalItem)
        parser = FestivalDataParser(
            model=config('MISTRAL_MODEL'),
            message=PROMPT,
            api_key=config('MISTRAL_API_KEY')
        )

        scraper = FestivalScraper(
            base_url=BASE_URL,
            saver=saver,
            fetcher=fetcher,
            parser=parser,
            validator=validator
        )

        arg_parser = argparse.ArgumentParser(
            description="Festival Scraper with dynamic log level"
        )

        arg_parser.add_argument(
            '-l', '--log-level',
            default='INFO',
            choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
            help='Set the logging level (default: INFO)'
        )

        args = arg_parser.parse_args()

        logger = Logger('Root', args.log_level)
        logger.logger.info("Starting Festival Scraper with log level: %s", args.log_level)

        for tool in [parser, fetcher, saver, validator, scraper]:
            tool.logger.set_log_level(args.log_level)

        await scraper.run(START_URL)

        await fetcher.close()


if __name__ == '__main__':
    asyncio.run(main())
