import json
import jsonlines

from utils.logger import Logger


class DataSaver:
    def __init__(self):
        self.logger = Logger('Saver')

    def save(self, items: list[dict], filename: str):
        with jsonlines.open(filename, mode='a') as writer:
            for item in items:
                writer.write(item)
                # self.logger.logger.info("Saved item: %s", json.dumps(item))

        # self.logger.logger.info("Saved %d items to %s", len(items), filename)

    def read(self, filename: str):
        with jsonlines.open(filename, mode='r') as reader:
            return list(reader)
