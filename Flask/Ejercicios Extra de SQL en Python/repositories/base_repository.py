from exceptions import NotFoundError


class BaseRepository:
    _COLUMNS = ()
    _ENTITY_LABEL = "Registro"

    def __init__(self, db_manager):
        self.db_manager = db_manager

    def _format_record(self, record):
        return dict(zip(self._COLUMNS, record))

    def _first_or_raise(self, results, record_id):
        if not results:
            raise NotFoundError(f"{self._ENTITY_LABEL} {record_id} no encontrado.")
        return self._format_record(results[0])

    def _first_or_none(self, results):
        if not results:
            return None
        return self._format_record(results[0])

    def _format_all(self, results):
        return [self._format_record(result) for result in results]

    def _all_or_none(self, results):
        if not results:
            return None
        return self._format_all(results)
