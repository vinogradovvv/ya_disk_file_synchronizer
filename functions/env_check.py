import os
import sys


def env_check() -> bool:
    """
    Checks environment variables
    """
    if not os.path.exists(".env"):
        sys.exit("Please copy env.template file to .env file and fill it.")

    if not os.getenv("YA_DISK_OAUTH_TOKEN"):
        sys.exit("Please fill yandex authenication token to the .env file")

    local_path = os.getenv("LOCAL_PATH")
    if not local_path or not local_path.endswith("/"):
        sys.exit(
            "Please fill path to local synchronise folder "
            "to the .env file with '/' in the end."
        )

    if not os.path.exists(os.getenv("LOCAL_PATH")) or (
        not os.path.isdir(os.getenv("LOCAL_PATH"))
    ):
        sys.exit("Incorrect path to local synchronise folder in the .env file")

    remote_path = os.getenv("YA_DISK_PATH")
    if not remote_path:
        sys.exit(
            "Please fill path to synchronise folder on the yandex disk "
            "to the .env file with '/' in the end."
        )
    elif not remote_path.endswith("/"):
        sys.exit(
            "Path to synchronise folder on the yandex disk must ends with rhe '/'."
        )

    if not os.getenv("SYNC_TIME_INTERVAL"):
        sys.exit("Please fill synchronisation interval in seconds to the .env file")

    try:
        message = "Incorrect syncronisation interval in the .env file"
        interval = float(os.getenv("SYNC_TIME_INTERVAL"))
        if interval <= 0:
            sys.exit(message)
    except ValueError:
        sys.exit(message)

    return True
