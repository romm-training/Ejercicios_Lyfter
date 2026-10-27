import csv, os
from pathlib import Path
from datetime import datetime
from infrastructure.backup_writer import BackupWriter
from exceptions import BackupError

class CsvBackupWriter(BackupWriter):
    def __init__(self, output_dir:str):
        self.output_dir = Path(output_dir)

    def write(self, table_name, headers, data) -> str:
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

            self.output_dir.mkdir(parents=True, exist_ok=True)

            file_name = self.output_dir / f"{table_name}_backup_{timestamp}.csv"

            with open(file_name, "w", encoding="utf-8", newline="") as file:
                writer = csv.DictWriter(file, headers)
                writer.writeheader()
                writer.writerows(data)
            return file_name.name
        except OSError as e:
            raise BackupError(f"No se pudo escribir el respaldo: {e}") from e

    