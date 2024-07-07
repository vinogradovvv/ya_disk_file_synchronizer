from sched import scheduler
from typing import Callable

from classes.synchronizer import Synchronizer


def schedule(
    task_scheduler: scheduler,
    sync_interval: float,
    sync_func: Callable,
    synchronizer: Synchronizer,
) -> None:
    """
    Implementation of sync loop
    """
    task_scheduler.enter(
        sync_interval,
        1,
        schedule,
        (task_scheduler, sync_interval, sync_func, synchronizer),
    )
    sync_func(synchronizer)
    print("sync")
