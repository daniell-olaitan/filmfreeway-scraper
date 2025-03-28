from utils.logger import Logger
from typing import NamedTuple, Any, Optional


class FestivalDataValidator:
    def __init__(self, item_type: type[NamedTuple]):
        self.item_type = item_type
        self.items_set: set[NamedTuple] = set()
        self.logger = Logger('Validator')

    def clean_item(self, item: dict[str, Any]) -> dict[str, Any]:
        return {
            k: v for k, v in item.items()
            if v
            if k in list(self.item_type.__annotations__.keys())
        }

    def validate_item(self, item: dict[str, Any]) -> Optional[NamedTuple]:
        fields = self.clean_item(item)

        # Make the item unique
        cleaned_item = {}
        for field_name, value in fields.items():
            field_name = field_name.strip().lower()
            if isinstance(value, str):
                value = value.strip().lower()

            cleaned_item[field_name] = value

        try:
            return self.item_type.from_dict(cleaned_item)
        except TypeError as e:
            self.logger.logger.error("Invalid fields: %s. Item skipped", e)
            return None

    def is_item_unique(self, item: NamedTuple) -> bool:
        if item in self.items_set:
            self.logger.logger.warning("Item is not unique. Item skipped.")
            return False

        self.items_set.add(item)
        return True
