import json

from mistralai import Mistral
from utils.logger import Logger
from playwright.async_api import Locator


class FestivalDataParser:
    def __init__(self, *, model: str, api_key: str):
        self._model = model
        self.logger = Logger('Parser')
        self._client = Mistral(api_key=api_key)

    async def exctract_details(self, prompt: str, data: str) -> dict:
        messages = [
            {
                'role': 'user',
                'content': prompt.format(data=data)
            }
        ]

        while True:
            try:
                response = await self._client.chat.complete_async(
                    model=self._model,
                    messages=messages,
                    response_format={
                        "type": "json_object",
                    }
                )

                break
            except Exception:
                self.logger.logger.debug("Retrying to extract data: %s")

        content = response.choices[0].message.content
        self.logger.logger.info("Extracted: %s", content)

        try:
            parsed_content = json.loads(content)
            return parsed_content
        except json.JSONDecodeError:
            self.logger.logger.error("Failed to parse response as JSON: %s", content)
            raise


    async def parse_text_content(self, data: Locator) -> list:
        return await data.all_inner_texts()

    async def parse_attr(self, data: Locator, attr: str) -> list:
        return await data.evaluate_all(
            f"els => els.map(el => el.getAttribute(\'{attr}\'))"
        )
