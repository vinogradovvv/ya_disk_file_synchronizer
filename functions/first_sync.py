from loguru import logger
from requests.exceptions import RequestException

from classes.synchronizer import Synchronizer


def first_sync(synchronizer: Synchronizer) -> bool:
    """
    Creates sync folder on the yandex disk if it does not exist
    """
    try:
        response = synchronizer.get_info()
    except RequestException:
        return False
    if response.status_code == 401:
        logger.error(
            "Unauthorized. Please check auth token in the .env files."
            "If token is correct, please check permissions on yandex disk service."
        )
        return False
    elif response.status_code == 404:
        synchronizer.create_folder()
        logger.debug("Cloud folder created")
        return True
    elif response.status_code == 200:
        logger.debug("Cloud folder exists")
        return True
