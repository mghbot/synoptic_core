"""Base plugin class for extending Synoptic Core functionality."""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from dataclasses import dataclass

from synoptic_core.models.logic_statement import LogicStatement
from synoptic_core.models.rule import Rule


@dataclass
class PluginMetadata:
    """Metadata for a plugin."""
    name: str
    version: str
    author: str
    description: str
    dependencies: List[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "name": self.name,
            "version": self.version,
            "author": self.author,
            "description": self.description,
            "dependencies": self.dependencies or []
        }


class BasePlugin(ABC):
    """Base class for Synoptic Core plugins."""
    
    def __init__(self):
        """Initialize the plugin."""
        self.metadata = self.get_metadata()
        self.custom_rules = []
    
    @abstractmethod
    def get_metadata(self) -> PluginMetadata:
        """Return plugin metadata.
        
        Returns:
            PluginMetadata object
        """
        pass
    
    @abstractmethod
    def initialize(self, config: Dict[str, Any]) -> None:
        """Initialize the plugin with configuration.
        
        Args:
            config: Plugin configuration dictionary
        """
        pass
    
    def get_custom_rules(self) -> List[Rule]:
        """Get custom rules provided by this plugin.
        
        Returns:
            List of Rule objects
        """
        return self.custom_rules
    
    def pre_process(self, text: str) -> str:
        """Pre-process text before main processing.
        
        Args:
            text: Input text
            
        Returns:
            Processed text
        """
        return text
    
    def post_process(self, statements: List[LogicStatement]) -> List[LogicStatement]:
        """Post-process generated statements.
        
        Args:
            statements: List of logic statements
            
        Returns:
            Processed statements
        """
        return statements
    
    def transform_statement(self, statement: LogicStatement) -> Optional[LogicStatement]:
        """Transform a single statement.
        
        Args:
            statement: Input logic statement
            
        Returns:
            Transformed statement or None to filter out
        """
        return statement
    
    def validate(self) -> bool:
        """Validate plugin configuration and state.
        
        Returns:
            True if valid, False otherwise
        """
        return bool(self.metadata and self.metadata.name)