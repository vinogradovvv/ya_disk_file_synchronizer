import json
import os
import time
from datetime import datetime
from multiprocessing import cpu_count
from multiprocessing.pool import ThreadPool
from os.path import isfile, join

from functions.md5_hash import compute_hash


def scan_folder() -> dict:
    """
    Scans folder, and computes hashes if it is needs
    """
    local_path = os.getenv("LOCAL_PATH")
    scan_file = os.getenv("SCAN_FILE")
    try:
        with open(scan_file, "r") as file:
            scan_data = json.load(file)
    except FileNotFoundError:
        scan_data = {}
        pool = ThreadPool(processes=cpu_count())
        for item in os.listdir(local_path):
            if isfile(join(local_path, item)):
                pool.apply_async(compute_hash, (item, scan_data))
        pool.close()
        pool.join()
        with open(scan_file, "w") as file:
            json.dump(scan_data, file, indent=4)
        return scan_data

    modified: bool = False
    deleted = []
    pool = ThreadPool(processes=cpu_count())
    for file in scan_data:
        if not os.path.exists(join(local_path, file)):
            modified = True
            deleted.append(file)
        elif (datetime.strptime(scan_data[file][0], "%a %b %d %H:%M:%S %Y")) < (
            datetime.strptime(
                time.ctime(os.path.getmtime(join(local_path, file))),
                "%a %b %d %H:%M:%S %Y",
            )
        ):
            modified = True
            pool.apply_async(compute_hash, (file, scan_data))
    pool.close()
    pool.join()
    pool = ThreadPool(processes=cpu_count())
    for file in os.listdir(local_path):
        if file not in scan_data.keys():
            modified = True
            pool.apply_async(compute_hash, (file, scan_data))
    pool.close()
    pool.join()

    if modified:
        for name in deleted:
            scan_data.pop(name)
        with open(scan_file, "w") as file:
            json.dump(scan_data, file, indent=4)
    return scan_data
