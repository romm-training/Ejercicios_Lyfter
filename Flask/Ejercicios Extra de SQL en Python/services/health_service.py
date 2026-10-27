from services.rules.health_rules import HealthCheck
from exceptions import HealthRuleError

class HealthService():
    def __init__(self, rules: list[HealthCheck]):
        self.rules = rules

    def validate_system_health(self) -> dict:
        results = {}

        for rule in self.rules:
            try:
                rule.run()
                results[rule.name] = "ok"
            except HealthRuleError as e:
                results[rule.name] = str(e)
        return {
            "healthy": all(v == "ok" for v in results.values()), "checks": results}
