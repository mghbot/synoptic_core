"""Pytest configuration and shared fixtures."""

import pytest
from synoptic_core import SynopticEngine
from synoptic_core.models.rule import Rule
from synoptic_core.models.logic_statement import LogicStatement


@pytest.fixture
def engine():
    """Create a Synoptic Engine instance."""
    return SynopticEngine()


@pytest.fixture
def sample_text():
    """Sample text for testing."""
    return "The cat is a mammal. The cat has fur. If it rains then the ground is wet."


@pytest.fixture
def sample_rules():
    """Sample rules for testing."""
    return [
        Rule(
            name="test_is_a",
            pattern=r"(\w+)\s+is\s+a\s+(\w+)",
            rule_type="regex",
            action={
                "predicate": "is_a",
                "statement_type": "classification"
            }
        ),
        Rule(
            name="test_has",
            pattern=r"(\w+)\s+has\s+(\w+)",
            rule_type="regex",
            action={
                "predicate": "has",
                "statement_type": "property"
            }
        )
    ]


@pytest.fixture
def sample_statement():
    """Sample logic statement."""
    return LogicStatement(
        subject="cat",
        predicate="is_a",
        object="mammal",
        statement_type="classification",
        confidence=0.9
    )