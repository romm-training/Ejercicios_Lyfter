from abc import ABC, abstractmethod

class BackupWriter(ABC):
    @abstractmethod
    def write(
        self, 
        table_name: str, 
        headers: list[str],
        data: list[dict]
    ) -> str:
        """Escribe el respaldo y devuelve su ubicación. Lanza BackupError si falla."""
