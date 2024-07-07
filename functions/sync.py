import os
from multiprocessing import cpu_count
from multiprocessing.pool import ThreadPool
from os.path import join

from loguru import logger
from requests.exceptions import RequestException

from classes.synchronizer import Synchronizer
from functions.scan_local_folder import scan_folder


def sync(synchronizer: Synchronizer) -> None:
    """
    Synchronise local and remote sync directory
    """
    try:
        remote_data = synchronizer.get_info().json()["_embedded"]["items"]
    except RequestException:
        logger.error(
            "Can't get remote directory info from server. Synchronisation aborted."
        )
        return
    remote_files = {file["name"]: file["md5"] for file in remote_data}
    local_path = os.getenv("LOCAL_PATH")
    local_files = scan_folder()
    pool = ThreadPool(processes=cpu_count())
    for file in local_files:
        if (
            file not in remote_files.keys()
            or local_files[file][1] != remote_files[file]
        ):
            pool.apply_async(synchronizer.load, (join(local_path, file),))
    pool.close()
    pool.join()
    for file in remote_files.keys() - local_files.keys():
        synchronizer.delete(file)
