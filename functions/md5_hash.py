import hashlib
import os
import time
from os.path import join


def compute_hash(filename: str, files_data_dict: dict) -> None:
    """
    Computes md5 hash of given file and puts result in the given dict
    """
    local_path = os.getenv("LOCAL_PATH")
    with open(join(local_path, filename), "rb") as file:
        md5 = hashlib.file_digest(file, "md5").hexdigest()
    mod_time = time.ctime(os.path.getmtime(join(local_path, filename)))
    files_data_dict[filename] = (mod_time, md5)
