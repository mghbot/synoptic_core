from .byte_parser import parse_to_bytes
from .rule_engine import apply_rules

def main():
    sample = "Hello"
    byte_list = parse_to_bytes(sample)
    print("Byte list:", byte_list)

    result = apply_rules(byte_list, "logic/rules.json")

    print("Rule Output:", result)

if __name__ == "__main__":
    main()
