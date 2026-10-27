from infrastructure.backup_writer import BackupWriter
from infrastructure.csv_backup_writer import CsvBackupWriter
from exceptions import BackupError

def create_backup_writer(writer_type: str, output_dir: str) -> BackupWriter:
    builders = {
        "csv": lambda: CsvBackupWriter(output_dir),
    }

    try:
        return builders[writer_type]()
    except KeyError:
        raise BackupError(f"BACKUP_WRITER invalido: {type!r}. Opciones: {list(builders)}")
