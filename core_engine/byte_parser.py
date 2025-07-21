from typing import List

def parse_to_bytes(text: str) -> List[int]:
    return [ord(char) for char in text]
