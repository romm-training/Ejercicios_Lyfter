import csv, os
from pathlib import Path
from datetime import datetime
from infrastructure.backup_writer import BackupWriter

class CsvBackupWriter(BackupWriter):
    def __init__(self, output_dir:str):
        self.output_dir = output_dir

    def write(self, table_name, headers, data) -> str:
        file_name = os.path.join(self.output_dir, f"{table_name}_{datetime.now()}.csv")
        with open(file_name, "w", encoding="utf-8", newline="") as file:
            writer = csv.DictWriter(file, headers)
            writer.writeheader()
            writer.writerows(data)
        return file_name

    