class BackupService():
    def __init__(self, repositories, backup_writer):
        self.repositories = repositories
        self.backup_writer = backup_writer

    def execute_backup(self):
        executed_backups = []
        for repo in self.repositories:
            table_name = repo.get_table_name()
            headers = repo.get_field_names()
            data = repo.get_all({})
            executed_backups.append(
                self.backup_writer.write(table_name, headers, data)
            )
        return executed_backups
