# Synoptic Core

A modular hybrid AI engine that uses symbolic logic, byte-level encoding, and dictionary-based rule matching.

## Features

- **Byte-level Encoding**: Efficient text processing at the byte level
- **Pattern Matching**: Flexible rule-based pattern matching
- **Symbolic Logic**: Generate structured logic statements
- **Plugin Architecture**: Extensible design for custom modules
- **CLI Interface**: Easy-to-use command-line interface

## Installation

```bash
pip install -e .
```

## Usage

### Command Line Interface

```bash
# Process text with default rules
synoptic process "Your text here"

# Apply specific rule set
synoptic process "Your text here" --rules custom_rules.json

# Show parsed logic statements
synoptic process "Your text here" --output-format verbose
```

### Python API

```python
from synoptic_core import SynopticEngine

# Initialize engine
engine = SynopticEngine()

# Process text
result = engine.process("Your text here")

# Access logic statements
for statement in result.statements:
    print(statement.format())
```

## Architecture

The Synoptic Core consists of several modular components:

1. **Byte Encoder**: Converts text to byte-level representation
2. **Parser**: Tokenizes and structures the input
3. **Rule Engine**: Applies pattern-matching rules
4. **Output Handler**: Formats and exports logic statements

## Development

```bash
# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Run tests with coverage
pytest --cov=synoptic_core
```