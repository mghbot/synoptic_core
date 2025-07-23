"""Output handler for formatting and exporting logic statements."""

from typing import List, Dict, Any, Optional
import json
from datetime import datetime
from dataclasses import dataclass, asdict

from synoptic_core.models.logic_statement import LogicStatement


@dataclass
class ProcessingResult:
    """Container for processing results."""
    statements: List[LogicStatement]
    processing_time: float
    timestamp: str
    metadata: Dict[str, Any]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            "statements": [stmt.to_dict() for stmt in self.statements],
            "processing_time": self.processing_time,
            "timestamp": self.timestamp,
            "metadata": self.metadata
        }
    
    def to_json(self) -> str:
        """Convert to JSON string."""
        return json.dumps(self.to_dict(), indent=2)


class OutputHandler:
    """Handles formatting and export of logic statements."""
    
    def __init__(self, default_format: str = "simple"):
        """Initialize OutputHandler.
        
        Args:
            default_format: Default output format
        """
        self.default_format = default_format
        self.formatters = {
            "simple": self._format_simple,
            "verbose": self._format_verbose,
            "json": self._format_json,
            "prolog": self._format_prolog,
            "rdf": self._format_rdf,
        }
    
    def format_output(self, statements: List[LogicStatement], 
                     format_type: Optional[str] = None,
                     processing_time: float = 0.0) -> ProcessingResult:
        """Format logic statements for output.
        
        Args:
            statements: List of logic statements
            format_type: Output format type
            processing_time: Time taken to process
            
        Returns:
            ProcessingResult object
        """
        format_type = format_type or self.default_format
        
        # Create metadata
        metadata = {
            "total_statements": len(statements),
            "statement_types": self._count_statement_types(statements),
            "average_confidence": self._calculate_average_confidence(statements),
            "format": format_type
        }
        
        return ProcessingResult(
            statements=statements,
            processing_time=processing_time,
            timestamp=datetime.utcnow().isoformat(),
            metadata=metadata
        )
    
    def export_statements(self, statements: List[LogicStatement], 
                         format_type: str, 
                         output_file: Optional[str] = None) -> str:
        """Export statements in specified format.
        
        Args:
            statements: List of logic statements
            format_type: Export format
            output_file: Optional file path for output
            
        Returns:
            Formatted string representation
        """
        formatter = self.formatters.get(format_type, self._format_simple)
        formatted_output = formatter(statements)
        
        if output_file:
            with open(output_file, 'w') as f:
                f.write(formatted_output)
        
        return formatted_output
    
    def _format_simple(self, statements: List[LogicStatement]) -> str:
        """Format statements in simple human-readable format."""
        lines = []
        for stmt in statements:
            lines.append(stmt.format())
        return "\n".join(lines)
    
    def _format_verbose(self, statements: List[LogicStatement]) -> str:
        """Format statements with detailed information."""
        lines = []
        for i, stmt in enumerate(statements, 1):
            lines.append(f"Statement #{i}")
            lines.append(f"  Type: {stmt.statement_type}")
            lines.append(f"  Subject: {stmt.subject}")
            lines.append(f"  Predicate: {stmt.predicate}")
            lines.append(f"  Object: {stmt.object}")
            lines.append(f"  Confidence: {stmt.confidence:.2f}")
            if stmt.metadata:
                lines.append(f"  Metadata: {json.dumps(stmt.metadata, indent=4)}")
            lines.append("")
        return "\n".join(lines)
    
    def _format_json(self, statements: List[LogicStatement]) -> str:
        """Format statements as JSON."""
        data = {
            "statements": [stmt.to_dict() for stmt in statements],
            "count": len(statements)
        }
        return json.dumps(data, indent=2)
    
    def _format_prolog(self, statements: List[LogicStatement]) -> str:
        """Format statements as Prolog facts."""
        lines = []
        for stmt in statements:
            # Clean values for Prolog
            subject = stmt.subject.lower().replace(" ", "_")
            predicate = stmt.predicate.lower().replace(" ", "_")
            obj = stmt.object.lower().replace(" ", "_")
            
            lines.append(f"{predicate}({subject}, {obj}).")
        
        return "\n".join(lines)
    
    def _format_rdf(self, statements: List[LogicStatement]) -> str:
        """Format statements as RDF triples."""
        lines = ["@prefix : <http://synoptic-core.ai/ontology#> ."]
        lines.append("")
        
        for stmt in statements:
            subject = f":{stmt.subject.replace(' ', '_')}"
            predicate = f":{stmt.predicate.replace(' ', '_')}"
            obj = f":{stmt.object.replace(' ', '_')}"
            
            lines.append(f"{subject} {predicate} {obj} .")
        
        return "\n".join(lines)
    
    def _count_statement_types(self, statements: List[LogicStatement]) -> Dict[str, int]:
        """Count occurrences of each statement type."""
        type_counts = {}
        for stmt in statements:
            type_counts[stmt.statement_type] = type_counts.get(stmt.statement_type, 0) + 1
        return type_counts
    
    def _calculate_average_confidence(self, statements: List[LogicStatement]) -> float:
        """Calculate average confidence score."""
        if not statements:
            return 0.0
        return sum(stmt.confidence for stmt in statements) / len(statements)