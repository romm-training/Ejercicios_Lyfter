class BackupService():
    def __init__(self, repositories, backup_writer):
        self.repositories = repositories
        self.backup_writers = backup_writer

    def execute_backup(self):
        executed_backups = []
        for repo in self.repositories:
            table_name = repo.__class__.__name__.split("_")[0]
            executed_backups.add(
                self.backup_writer.write(table_name, repo.get_all())
            )
