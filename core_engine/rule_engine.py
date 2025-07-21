import json
from typing import List

def apply_rules(byte_list: List[int], rules_path: str = "logic/rules.json") -> List[str]:
    with open(rules_path, "r") as file:
        rules = json.load(file)

    results = []
    for byte in byte_list:
        rule = rules.get(str(byte))
        if rule:
            results.append(rule)
        else:
            results.append(f"UNKNOWN({byte})")
    return results
