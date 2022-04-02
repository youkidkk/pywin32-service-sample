import logging
import logging.config
import signal
from threading import Event, Thread

from child.log_loop import LogLoop

logger = logging.getLogger(__name__)


class Main:
    def __init__(self, stop_event):
        self.stop_event: Event = stop_event

    def run(self):
        logger.info("Main: start.")

        th1 = Thread(target=LogLoop("Tread1", 3, self.stop_event).run)
        th1.start()
        th2 = Thread(target=LogLoop("Tread2", 4, self.stop_event).run)
        th2.start()
        th3 = Thread(target=LogLoop("Tread3", 5, self.stop_event).run)
        th3.start()

        while not self.stop_event.wait(timeout=3):
            logger.info("Main: Running...")
        th1.join()
        th2.join()
        th3.join()
        logger.info("Main: End.")


stop_event = Event()


def signal_handler(signum, _):
    logger.info(f"Signal: {signum}")
    stop_event.set()


if __name__ == "__main__":
    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGINT, signal_handler)

    m = Main(stop_event)
    m.run()
