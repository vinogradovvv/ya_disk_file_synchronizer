from abc import ABC, abstractmethod
from typing import Any, Optional


class Synchronizer(ABC):
    """
    Abstraction to help implement services other than yandex
    """

    @abstractmethod
    def load(self, path):
        pass

    @abstractmethod
    def reload(self, path):
        pass

    @abstractmethod
    def delete(self, filename):
        pass

    @abstractmethod
    def get_info(self):
        pass

    @abstractmethod
    def create_folder(self, path: Optional[Any] = None):
        pass
