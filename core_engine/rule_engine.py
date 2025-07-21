import json

def apply_rules_from_file(byte_values: list[int], rule_file_path: str) -> list[str]:
    """
    Applies rules from a JSON file to a list of byte values.
    Converts byte values into characters based on the rules.

    Example rule file format:
    {
        "65": "A",
        "66": "B",
        "97": "a"
    }
    """
    with open(rule_file_path, "r") as f:
        rules = json.load(f)

    return [rules.get(str(byte), '?') for byte in byte_values]
