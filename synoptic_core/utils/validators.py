"""Validation utilities for Synoptic Core."""

import re
from typing import Union, List


def validate_text_input(text: Union[str, bytes], max_length: int = 1_000_000) -> bool:
    """Validate text input.
    
    Args:
        text: Input text or bytes
        max_length: Maximum allowed length
        
    Returns:
        True if valid
        
    Raises:
        ValueError: If validation fails
    """
    if not text:
        raise ValueError("Text input cannot be empty")
    
    if isinstance(text, bytes):
        if len(text) > max_length:
            raise ValueError(f"Input exceeds maximum length of {max_length} bytes")
    else:
        if len(text.encode('utf-8')) > max_length:
            raise ValueError(f"Input exceeds maximum length of {max_length} bytes")
    
    return True


def validate_rule_pattern(pattern: str, rule_type: str) -> bool:
    """Validate rule pattern based on rule type.
    
    Args:
        pattern: Pattern string
        rule_type: Type of rule
        
    Returns:
        True if valid
        
    Raises:
        ValueError: If validation fails
    """
    if not pattern:
        raise ValueError("Pattern cannot be empty")
    
    if rule_type == "regex":
        try:
            re.compile(pattern)
        except re.error as e:
            raise ValueError(f"Invalid regex pattern: {e}")
    
    elif rule_type == "token":
        if not pattern.replace(" ", "").isalnum():
            raise ValueError("Token pattern must contain only alphanumeric characters and spaces")
    
    elif rule_type == "sequence":
        if len(pattern.split()) < 2:
            raise ValueError("Sequence pattern must contain at least 2 tokens")
    
    return True


def validate_confidence_score(score: float) -> bool:
    """Validate confidence score.
    
    Args:
        score: Confidence score
        
    Returns:
        True if valid
        
    Raises:
        ValueError: If validation fails
    """
    if not isinstance(score, (int, float)):
        raise ValueError("Confidence score must be a number")
    
    if not 0 <= score <= 1:
        raise ValueError("Confidence score must be between 0 and 1")
    
    return True


def validate_statement_components(subject: str, predicate: str, obj: str) -> bool:
    """Validate logic statement components.
    
    Args:
        subject: Statement subject
        predicate: Statement predicate
        obj: Statement object
        
    Returns:
        True if valid
        
    Raises:
        ValueError: If validation fails
    """
    components = {"subject": subject, "predicate": predicate, "object": obj}
    
    for name, value in components.items():
        if not value:
            raise ValueError(f"Statement {name} cannot be empty")
        
        if not isinstance(value, str):
            raise ValueError(f"Statement {name} must be a string")
        
        if len(value) > 1000:
            raise ValueError(f"Statement {name} exceeds maximum length of 1000 characters")
    
    return True


def validate_plugin_metadata(metadata: dict) -> bool:
    """Validate plugin metadata.
    
    Args:
        metadata: Plugin metadata dictionary
        
    Returns:
        True if valid
        
    Raises:
        ValueError: If validation fails
    """
    required_fields = ["name", "version", "author", "description"]
    
    for field in required_fields:
        if field not in metadata:
            raise ValueError(f"Plugin metadata missing required field: {field}")
        
        if not metadata[field]:
            raise ValueError(f"Plugin metadata field '{field}' cannot be empty")
    
    # Validate version format (basic semver)
    version_pattern = r'^\d+\.\d+\.\d+$'
    if not re.match(version_pattern, metadata["version"]):
        raise ValueError("Plugin version must follow semantic versioning (e.g., 1.0.0)")
    
    return True