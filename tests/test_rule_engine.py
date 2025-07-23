"""Tests for RuleEngine module."""

import pytest
from synoptic_core.core.rule_engine import RuleEngine
from synoptic_core.core.parser import Parser
from synoptic_core.models.rule import Rule


class TestRuleEngine:
    """Test cases for RuleEngine."""
    
    def test_builtin_rules(self):
        """Test that built-in rules are loaded."""
        engine = RuleEngine()
        rules = engine.get_builtin_rules()
        
        assert len(rules) > 0
        assert any(r.name == "is_a_relation" for r in rules)
        assert any(r.name == "has_relation" for r in rules)
    
    def test_apply_regex_rule(self):
        """Test applying regex rule."""
        engine = RuleEngine()
        parser = Parser()
        
        text = "The cat is a mammal"
        parsed_data = parser.parse(text.encode('utf-8'))
        
        statements = engine.apply_rules(parsed_data)
        
        assert len(statements) > 0
        assert any(s.subject == "cat" and s.predicate == "is_a" and s.object == "mammal" 
                  for s in statements)
    
    def test_custom_rule(self):
        """Test applying custom rule."""
        engine = RuleEngine()
        parser = Parser()
        
        custom_rule = Rule(
            name="custom_test",
            pattern=r"(\w+)\s+loves\s+(\w+)",
            rule_type="regex",
            action={
                "predicate": "loves",
                "statement_type": "emotion"
            }
        )
        
        text = "Alice loves Bob"
        parsed_data = parser.parse(text.encode('utf-8'))
        
        statements = engine.apply_rules(parsed_data, [custom_rule])
        
        assert len(statements) == 1
        assert statements[0].subject == "Alice"
        assert statements[0].predicate == "loves"
        assert statements[0].object == "Bob"
    
    def test_confidence_scores(self):
        """Test confidence score calculation."""
        engine = RuleEngine()
        parser = Parser()
        
        text = "The cat is a mammal. The cat has fur."
        parsed_data = parser.parse(text.encode('utf-8'))
        
        statements = engine.apply_rules(parsed_data)
        
        # All statements should have confidence scores
        assert all(0 <= s.confidence <= 1 for s in statements)
    
    def test_duplicate_merging(self):
        """Test that duplicate statements are merged."""
        engine = RuleEngine()
        parser = Parser()
        
        # Text that would generate duplicate statements
        text = "A cat is a mammal. The cat is a mammal."
        parsed_data = parser.parse(text.encode('utf-8'))
        
        statements = engine.apply_rules(parsed_data)
        
        # Should have unique statements
        unique_keys = set((s.subject, s.predicate, s.object) for s in statements)
        assert len(unique_keys) == len(statements)
    
    def test_token_rule(self):
        """Test token-based rule matching."""
        engine = RuleEngine()
        parser = Parser()
        
        rule = Rule(
            name="important_words",
            pattern="important critical",
            rule_type="token",
            action={
                "predicate": "is_important",
                "statement_type": "annotation"
            }
        )
        
        text = "This is an important document"
        parsed_data = parser.parse(text.encode('utf-8'))
        
        statements = engine.apply_rules(parsed_data, [rule])
        
        assert len(statements) > 0
        assert any(s.subject == "important" for s in statements)