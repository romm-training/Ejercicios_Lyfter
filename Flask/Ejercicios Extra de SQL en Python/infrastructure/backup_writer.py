from abc import ABC, abstractmethod

class BackupWriter(ABC):
    @abstractmethod
    def write(self, table_name: str, data: list[dict]) -> str:
        pass
