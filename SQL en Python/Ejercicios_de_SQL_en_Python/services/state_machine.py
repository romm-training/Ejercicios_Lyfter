import os
from dataclasses import dataclass
from pathlib import Path

import yaml

#from services.rules import car_rental_rules, car_rules, user_rules
from repositories.car_repository import CarRepository
from repositories.car_rental_repository import CarRentalRepository
from repositories.user_repository import UserRepository

DEFAULT_ENCODING = "utf-8"

class InvalidTransitionError(Exception):
    pass

class BussinessRuleError(Exception):
    pass

GUARDS, EFFECTS = {}, {}

def _register(registry, name):
    def decorator(fn):
        if name in registry:
            raise ValueError(f"'{name}' ya está registrado.")
        registry[name] = fn
        return fn
    return decorator

def guard(name):
    return _register(GUARDS, name)

def effect(name):
    return _register(EFFECTS, name)

ENTITIES = {
    "car_rental": {"repo": CarRentalRepository, "column": "status"},
    "car": {"repo": CarRepository, "column": "status"},
    "user": {"repo": UserRepository, "column": "account_status"},
}

@dataclass
class Context:
    entity: str
    target_status: str
    repos: dict
    record: dict | None = None
    data: dict | None = None 

def load_transitions(path):
    with open(path, encoding=DEFAULT_ENCODING) as f:
        config = yaml.safe_load(f)

    table, initial = {}, {}
    for entity, spec in config.items():
        if entity not in ENTITIES:
            raise ValueError(f"Entidad desconocida: {entity}")
        states = spec["states"]
        if len(states) != len(set(states)):
            raise ValueError(f"Estados duplicados para la entidad {entity}")

        for t in spec["transitions"]:
            origin, target = t["from"], t["to"]
            
            for s in (origin, target):
                if s is not None and s not in states:
                    raise ValueError(f"Estado '{s}' no definido para la entidad {entity}")
            
            for name in t.get("guards", []):
                if name not in GUARDS:
                    raise ValueError(f"Guardia '{name}' no registrado para la entidad {entity}")
            
            for name in t.get("effects", []):
                if name not in EFFECTS:
                    raise ValueError(f"Efecto '{name}' no registrado para la entidad {entity}")
            
            key = (entity, origin, target)
            if key in table:
                raise ValueError(f"Transición duplicada: {key}")
            table[key] = t

            if origin is None:
                if entity in initial:
                    raise ValueError(f"Estado inicial duplicado para la entidad {entity}")
                initial[entity] = target

    return table, initial


class StateMachine:
    def __init__(self, db, table, initial):
        self.db = db
        self.table = table
        self.initial = initial

    def _repos(self):
        return {name: spec["repo"](self.db) for name, spec in ENTITIES.items()}

    def _find(self, entity, current_status, target_status):
        t = self.table.get((entity, current_status, target_status))
        if t is None:
            raise InvalidTransitionError(f"No se puede cambiar el estado de {entity} de {current_status} a {target_status}")
        return t

    @staticmethod
    def _run(names, registry, ctx):
        for name in names:
            registry[name](ctx)

    def change_status(self, entity, record_id, target_status):
        column = ENTITIES[entity]["column"]
        with self.db.transaction():
            repos = self._repos()
            repo = repos[entity]
            record = repo.get_by_id_for_update(record_id)
            current_status = record[column]

            t = self._find(entity, current_status, target_status)

            ctx = Context(entity=entity, target_status=target_status, repos=repos, record=record)

            self._run(t.get("guards",[]), GUARDS, ctx)

            repo.update_status(record_id, target_status)

            ctx.record = {**record, column: target_status}
            self._run(t.get("effects",[]), EFFECTS, ctx)

    def create(self, entity, data):
        column = ENTITIES[entity]["column"]
        target_status = self.initial[entity]
        with self.db.transaction():
            repos = self._repos()
            t = self._find(entity, None, target_status)
            ctx = Context(entity=entity, target_status=target_status, repos=repos, data=data)
            self._run(t.get("guards",[]), GUARDS, ctx)

            ctx.record = repos[entity].create({**data, column: target_status})
            self._run(t.get("effects",[]), EFFECTS, ctx)

            return ctx.record

def build_state_machine(db):
    config_path = Path(__file__).resolve().parent.parent / os.environ["STATUS_TRANSITIONS_PATH"]
    from services.rules import car_rental_rules, car_rules, user_rules
    table, initial = load_transitions(config_path)
    return StateMachine(db, table, initial)

            