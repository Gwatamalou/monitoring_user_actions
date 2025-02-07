from time import sleep


import json

from src.settings import logger
from src.repositories.redis_repository.base import RedisRepositoryBase


class EventProcessor(RedisRepositoryBase):

    @staticmethod
    def processor_event(event_data):
        logger.debug(f"Event: {event_data}")


    def event_worker(self):
        while True:
            event_json = self.client.rpop("event_queue")
            if event_json:
                event = json.loads(event_json)
                self.processor_event(event)
            else:
                sleep(1)

if __name__ == "__main__":
    print("Запуск обработчика событий...")
    r = EventProcessor()
    r.event_worker()


