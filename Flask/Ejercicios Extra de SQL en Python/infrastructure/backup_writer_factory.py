from services.backup_writer import BackupWriter
from infrastructure.csv_backup_writer import CsvBackupWriter
from exceptions import ConfigurationError

def create_backup_writer(writer_type: str, output_dir: str) -> BackupWriter:
    builders = {
        "csv": lambda: CsvBackupWriter(output_dir),
    }

    try:
        return builders[writer_type]()
    except KeyError:
        raise ConfigurationError(f"BACKUP_WRITER invalido: {writer_type}. Opciones: {list(builders)}")
