from time import sleep
import json

from src.settings import logger
from src.repositories.redis_repository.base import RedisRepositoryBase


class EventProcessor(RedisRepositoryBase):
    """
    Класс для обработки событий из очереди Redis.
    Наследуется от базового класса RedisRepositoryBase.
    """

    @staticmethod
    def processor_event(event_data):
        """
        Обрабатывает данные события, записывая их в журнал.

        :param event_data: Данные события, которые необходимо обработать.
        """
        logger.debug(f"Event: {event_data}")

    def event_worker(self):
        """
        Рабочий процесс, который извлекает события из очереди Redis и передает их на обработку.

        Цикл будет продолжаться бесконечно, пока не будут обработаны все события в очереди.
        Если очередь пуста, поток засыпает на 1 секунду.
        """
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
