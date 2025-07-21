from dataclasses import dataclass

@dataclass
class Rule:
    antecedents: list[str]
    consequent: str

class ForwardChainingInferenceEngine:
    def __init__(self, rules: list[Rule], facts: set[str]):
        self.rules = rules
        self.facts = set(facts)
        self.inferred = set()

    def run(self, goal=None):
        applied_rules = []

        while True:
            applied = False
            for rule in self.rules:
                if rule.consequent in self.facts:
                    continue  # Already known

                if all(antecedent in self.facts for antecedent in rule.antecedents):
                    self.facts.add(rule.consequent)
                    self.inferred.add(rule.consequent)
                    applied_rules.append(rule)
                    applied = True

                    if goal and rule.consequent == goal:
                        return True  # Goal achieved

            if not applied:
                break

        return goal in self.facts if goal else True

    def get_inferred_facts(self):
        return self.inferred
