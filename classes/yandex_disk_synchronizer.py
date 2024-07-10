import os
from typing import Optional

import requests
from dotenv import load_dotenv
from loguru import logger

from classes.synchronizer import Synchronizer


class YandexDiskSynchronizer(Synchronizer):
    """
    Provides methods to work with yandex disk service.
    """

    def __init__(self):
        load_dotenv()
        self.url = os.getenv("YA_DISK_URL")
        self.token = os.getenv("YA_DISK_OAUTH_TOKEN")
        self.cloud_path = os.getenv("YA_DISK_PATH")
        self.headers = {"Content-Type": "application/json", "Authorization": self.token}

    def load(self, path: str) -> None:
        """
        Loads files to the yandex disk.
        """
        with requests.session() as session:
            params = {
                "path": f"{self.cloud_path}{os.path.basename(path)}",
                "overwrite": True,
            }
            try:
                response = session.get(
                    url=f"{self.url}resources/upload",
                    params=params,
                    headers=self.headers,
                    timeout=5,
                )
            except requests.exceptions.RequestException as exc:
                logger.debug(exc)

            upload_link = response.json()["href"]
            try:
                file = open(path, "rb")
            except OSError as exc:
                logger.debug(exc)
            with file:
                try:
                    session.put(
                        url=upload_link, headers=self.headers, data=file, timeout=5
                    )
                    logger.info(f"File {os.path.basename(path)} synced.")
                    return
                except requests.exceptions.RequestException as exc:
                    logger.error(f"File {os.path.basename(path)} didn't sync.")
                    logger.debug(exc)

    def reload(self, path: str):
        """Same as load method."""
        return self.load(path=path)

    def delete(self, filename: str) -> None:
        """
        Deletes file from the yandex disk.
        """
        with requests.session() as session:
            params = {"path": f"{self.cloud_path}{filename}"}
            try:
                session.delete(
                    url=f"{self.url}resources",
                    headers=self.headers,
                    params=params,
                    timeout=5,
                )
                logger.info(f"File {filename} deleted")
                return
            except requests.exceptions.RequestException:
                logger.error(f"File {filename} didn't delete")

    def get_info(self) -> requests.Response:
        with requests.session() as session:
            params = {"path": self.cloud_path}
            try:
                response = session.get(
                    url=f"{self.url}resources",
                    headers=self.headers,
                    params=params,
                    timeout=5,
                )
                return response
            except requests.exceptions.RequestException as exc:
                logger.debug("Can't get remote directory info from server.")
                raise exc

    def create_folder(self, path: Optional[str] = None) -> requests.Response:
        """
        Creates folder on the yandex disk
        return: requests.Response
        """
        with requests.session() as session:
            if not path:
                dir_path = self.cloud_path
            else:
                dir_path = path
            params = {"path": dir_path}
            try:
                response = session.put(
                    url=f"{self.url}resources",
                    headers=self.headers,
                    params=params,
                    timeout=5,
                )
                logger.info(f"Directory {dir_path} created")
                return response
            except requests.exceptions.RequestException:
                logger.error(f"Directory {dir_path} didn't create")
