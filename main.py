import os
import time
from sched import scheduler

from dotenv import load_dotenv
from loguru import logger

from classes.yandex_disk_synchronizer import YandexDiskSynchronizer
from functions.env_check import env_check
from functions.first_sync import first_sync
from functions.schedule import schedule
from functions.sync import sync


def main() -> None:
    """
    Main synchronizer loop.
    """
    load_dotenv()
    env_check()
    synchronizer = YandexDiskSynchronizer()
    sync_interval = float(os.getenv("SYNC_TIME_INTERVAL"))
    logger.add(
        "synchronizer.log",
        format="synchronizer {time:DD MM YYYY HH:mm:ss} {level} {message}",
        level="INFO",
    )
    while not first_sync(synchronizer):
        logger.debug("Can't get remote directory info from server.")
        time.sleep(sync_interval)
    logger.info(f'Start with directory {os.getenv("LOCAL_PATH")}')
    sync_scheduler = scheduler(time.time, time.sleep)
    sync_scheduler.enter(
        sync_interval, 1, schedule, (sync_scheduler, sync_interval, sync, synchronizer)
    )
    sync_scheduler.run()


if __name__ == "__main__":
    main()
