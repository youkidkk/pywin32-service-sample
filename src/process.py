import logging
import logging.config
import signal
from threading import Event

import yaml

logger = logging.getLogger(__name__)


class Process:
    def __init__(self, stop_event):
        self.stop_event: Event = stop_event

    def run(self):
        logger.info("Process: 開始しました。")

        while not self.stop_event.wait(timeout=3):
            logger.info("Process: 実行中です。")
        logger.info("Process: 終了しました。")


stop_event = Event()


def signal_handler(signum, _):
    logger.info(f"Signal: {signum}")
    stop_event.set()


if __name__ == "__main__":
    with open("configs/log_conf.yml") as f:
        logging.config.dictConfig(yaml.unsafe_load(f.read()))

    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGINT, signal_handler)

    m = Process(stop_event)
    m.run()
