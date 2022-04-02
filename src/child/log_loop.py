from logging import getLogger
from threading import Event

logger = getLogger(__name__)


class LogLoop:
    def __init__(self, name, timeout, stop_event):
        self.name: str = name
        self.timeout: int = timeout
        self.stop_event: Event() = stop_event

    def run(self):
        logger.info(f"{self.name}: Start.")
        while not self.stop_event.wait(timeout=self.timeout):
            logger.info(f"{self.name}: Running...")
        logger.info(f"{self.name}: End.")
