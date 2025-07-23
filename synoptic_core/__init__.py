"""Synoptic Core - A modular hybrid AI engine for symbolic logic processing."""

from synoptic_core.core.byte_encoder import ByteEncoder
from synoptic_core.core.parser import Parser
from synoptic_core.core.rule_engine import RuleEngine
from synoptic_core.core.output_handler import OutputHandler
from synoptic_core.models.logic_statement import LogicStatement
from synoptic_core.models.rule import Rule

__version__ = "0.1.0"
__all__ = [
    "SynopticEngine",
    "ByteEncoder",
    "Parser",
    "RuleEngine",
    "OutputHandler",
    "LogicStatement",
    "Rule",
]


class SynopticEngine:
    """Main engine that orchestrates the symbolic logic processing pipeline."""
    
    def __init__(self, config=None):
        """Initialize the Synoptic Engine.
        
        Args:
            config: Optional configuration dictionary
        """
        self.byte_encoder = ByteEncoder()
        self.parser = Parser()
        self.rule_engine = RuleEngine()
        self.output_handler = OutputHandler()
        
    def process(self, text, rules=None):
        """Process text through the complete pipeline.
        
        Args:
            text: Input text to process
            rules: Optional list of Rule objects
            
        Returns:
            ProcessingResult object containing logic statements
        """
        # Encode text to bytes
        byte_data = self.byte_encoder.encode(text)
        
        # Parse byte data
        parsed_data = self.parser.parse(byte_data)
        
        # Apply rules
        logic_statements = self.rule_engine.apply_rules(parsed_data, rules)
        
        # Format output
        return self.output_handler.format_output(logic_statements)