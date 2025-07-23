"""Tests for OutputHandler module."""

import pytest
import json
from synoptic_core.core.output_handler import OutputHandler, ProcessingResult
from synoptic_core.models.logic_statement import LogicStatement


class TestOutputHandler:
    """Test cases for OutputHandler."""
    
    def test_format_output(self):
        """Test basic output formatting."""
        handler = OutputHandler()
        statements = [
            LogicStatement(
                subject="cat",
                predicate="is_a",
                object="mammal",
                statement_type="classification",
                confidence=0.9
            )
        ]
        
        result = handler.format_output(statements, processing_time=0.1)
        
        assert isinstance(result, ProcessingResult)
        assert result.statements == statements
        assert result.processing_time == 0.1
        assert result.metadata["total_statements"] == 1
    
    def test_simple_format(self):
        """Test simple format output."""
        handler = OutputHandler()
        statements = [
            LogicStatement(
                subject="cat",
                predicate="is_a",
                object="mammal",
                statement_type="classification"
            )
        ]
        
        output = handler.export_statements(statements, "simple")
        assert output == "(cat, is_a, mammal)"
    
    def test_json_format(self):
        """Test JSON format output."""
        handler = OutputHandler()
        statements = [
            LogicStatement(
                subject="cat",
                predicate="is_a",
                object="mammal",
                statement_type="classification"
            )
        ]
        
        output = handler.export_statements(statements, "json")
        data = json.loads(output)
        
        assert "statements" in data
        assert data["count"] == 1
        assert data["statements"][0]["subject"] == "cat"
    
    def test_prolog_format(self):
        """Test Prolog format output."""
        handler = OutputHandler()
        statements = [
            LogicStatement(
                subject="cat",
                predicate="is_a",
                object="mammal",
                statement_type="classification"
            )
        ]
        
        output = handler.export_statements(statements, "prolog")
        assert output == "is_a(cat, mammal)."
    
    def test_rdf_format(self):
        """Test RDF format output."""
        handler = OutputHandler()
        statements = [
            LogicStatement(
                subject="cat",
                predicate="is_a",
                object="mammal",
                statement_type="classification"
            )
        ]
        
        output = handler.export_statements(statements, "rdf")
        assert ":cat :is_a :mammal ." in output
    
    def test_verbose_format(self):
        """Test verbose format output."""
        handler = OutputHandler()
        statements = [
            LogicStatement(
                subject="cat",
                predicate="is_a",
                object="mammal",
                statement_type="classification",
                confidence=0.9
            )
        ]
        
        output = handler.export_statements(statements, "verbose")
        
        assert "Statement #1" in output
        assert "Type: classification" in output
        assert "Subject: cat" in output
        assert "Confidence: 0.90" in output
    
    def test_metadata_calculation(self):
        """Test metadata calculation."""
        handler = OutputHandler()
        statements = [
            LogicStatement("cat", "is_a", "mammal", "classification", 0.8),
            LogicStatement("dog", "is_a", "mammal", "classification", 0.9),
            LogicStatement("cat", "has", "fur", "property", 0.7)
        ]
        
        result = handler.format_output(statements)
        
        assert result.metadata["total_statements"] == 3
        assert result.metadata["average_confidence"] == pytest.approx(0.8, rel=1e-2)
        assert result.metadata["statement_types"]["classification"] == 2
        assert result.metadata["statement_types"]["property"] == 1