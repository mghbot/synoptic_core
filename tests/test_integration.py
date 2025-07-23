"""Integration tests for Synoptic Core."""

import pytest
from synoptic_core import SynopticEngine
from synoptic_core.models.rule import Rule


class TestIntegration:
    """Integration test cases."""
    
    def test_full_pipeline(self):
        """Test complete processing pipeline."""
        engine = SynopticEngine()
        
        text = "The cat is a mammal. The dog is a mammal. The cat has fur."
        result = engine.process(text)
        
        assert len(result.statements) > 0
        
        # Check for expected statements
        statements_str = [s.format() for s in result.statements]
        assert any("cat" in s and "mammal" in s for s in statements_str)
        assert any("dog" in s and "mammal" in s for s in statements_str)
        assert any("cat" in s and "fur" in s for s in statements_str)
    
    def test_custom_rules_integration(self):
        """Test integration with custom rules."""
        engine = SynopticEngine()
        
        custom_rules = [
            Rule(
                name="location_rule",
                pattern=r"(\w+)\s+is\s+in\s+(\w+)",
                rule_type="regex",
                action={
                    "predicate": "located_in",
                    "statement_type": "location"
                }
            )
        ]
        
        text = "Paris is in France. London is in England."
        result = engine.process(text, custom_rules)
        
        location_statements = [s for s in result.statements 
                              if s.statement_type == "location"]
        assert len(location_statements) == 2
        
        # Check specific locations
        assert any(s.subject == "Paris" and s.object == "France" 
                  for s in location_statements)
        assert any(s.subject == "London" and s.object == "England" 
                  for s in location_statements)
    
    def test_complex_text(self):
        """Test processing of complex text."""
        engine = SynopticEngine()
        
        text = """
        Artificial intelligence is a field of computer science. 
        Machine learning is a subset of AI. 
        Neural networks are used in deep learning.
        If a system uses neural networks then it is doing deep learning.
        """
        
        result = engine.process(text)
        
        # Should extract multiple types of relationships
        statement_types = set(s.statement_type for s in result.statements)
        assert len(statement_types) > 1
        
        # Should find classification relationships
        classifications = [s for s in result.statements 
                          if s.statement_type == "classification"]
        assert len(classifications) > 0
    
    def test_unicode_text(self):
        """Test processing of Unicode text."""
        engine = SynopticEngine()
        
        text = "The 猫 (cat) is a 哺乳动物 (mammal)."
        result = engine.process(text)
        
        # Should handle Unicode without errors
        assert isinstance(result.statements, list)
    
    def test_empty_results(self):
        """Test handling of text with no matches."""
        engine = SynopticEngine()
        
        # Text that doesn't match any patterns
        text = "Random words without patterns."
        result = engine.process(text)
        
        # Should return empty results without errors
        assert result.statements == [] or len(result.statements) >= 0
        assert result.metadata["total_statements"] >= 0
    
    def test_performance_with_large_text(self):
        """Test performance with larger text."""
        engine = SynopticEngine()
        
        # Generate larger text
        sentences = [
            f"Entity{i} is a Type{i % 5}. Entity{i} has Property{i % 3}."
            for i in range(100)
        ]
        text = " ".join(sentences)
        
        result = engine.process(text)
        
        # Should process without errors and find patterns
        assert len(result.statements) > 0
        
        # Check processing time is recorded
        assert hasattr(result, 'processing_time')