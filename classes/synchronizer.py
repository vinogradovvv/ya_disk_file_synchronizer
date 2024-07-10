from abc import ABC, abstractmethod
from typing import Any, Optional


class Synchronizer(ABC):
    """
    Abstraction to help implement services other than yandex
    """

    @abstractmethod
    def load(self, path):
        raise NotImplementedError("Method not implemented.")

    @abstractmethod
    def reload(self, path):
        raise NotImplementedError("Method not implemented.")

    @abstractmethod
    def delete(self, filename):
        raise NotImplementedError("Method not implemented.")

    @abstractmethod
    def get_info(self):
        raise NotImplementedError("Method not implemented.")

    @abstractmethod
    def create_folder(self, path: Optional[Any] = None):
        raise NotImplementedError("Method not implemented.")
