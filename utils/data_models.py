from typing import NamedTuple

PROMPT = """Extract structured data from the following user input:

{data}

Extraction Instructions:
Awards (awards): Identify and extract all award titles mentioned in the text. These should be specific awards given at the festival.

Categories (categories): Extract the main competition categories (e.g., Short, Experimental, Documentary, Fiction). Ignore subcategories.

Festival Info (festival_info): Summarize the festival's mission or purpose, typically found at the beginning of the text. Ensure it is concise and meaningful.

Important Dates (important_dates): Extract key festival-related dates, including application deadlines, festival event dates, and selection announcement dates. Keep only essential ones.

Output Format Example:
{{
  "awards": [
    "Best International Animation Film Award",
    "Best International Experimental Film Award",
    "Short Is Life International Best Short Film Award",
    "Short Is Life National Best Short Film Award",
    "Camera Eye International Best Documentary Award",
    "Camera Eye National Best Documentary Award",
    "SIYAD Best Documentary Award",
    "SIYAD Best Short Film Award",
    "Golden Reel International Best Feature Film Award",
    "Golden Reel National Best Feature Film Award",
    "Biket İlhan Best Director Award"
  ],
  "categories": ["Short", "Experimental", "Documentary", "Fiction"],
  "festival_info": "IWFFT aims to make women directors and their films visible by bringing together female directors and female film workers in the first week of March every year within the scope of 8 March International Working Women's Day.",
  "important_dates": ["8th - 13th February 2025", "15th January 2025"]
}}

Ensure the extracted data adheres to the specified structure and accurately represents the relevant information.
Return your response in JSON format.
"""


class FestivalItem(NamedTuple):
    festival_name: str
    festival_info: str | None = None
    deadlines: tuple[str, ...] | None = None
    awards: tuple[str, ...] | None = None
    categories: tuple[str, ...] | None = None
    important_dates: tuple[str, ...] | None = None

    @classmethod
    def from_dict(cls, data: dict[str, list[str] | str | None]):
        """Convert dictionary with lists into an immutable NamedTuple instance."""
        return cls(
            festival_name=data.get("festival_name", ""),
            festival_info=data.get("festival_info"),
            deadlines=tuple(data.get("deadlines", [])) if data.get("deadlines") else None,
            awards=tuple(data.get("awards", [])) if data.get("awards") else None,
            categories=tuple(data.get("categories", [])) if data.get("categories") else None,
            important_dates=tuple(data.get("important_dates", [])) if data.get("important_dates") else None
        )
