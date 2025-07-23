"""Logic statement model."""

from typing import Dict, Any, Optional
from dataclasses import dataclass, field, asdict
from datetime import datetime


@dataclass(unsafe_hash=True)
class LogicStatement:
    """Represents a structured logic statement."""
    
    subject: str
    predicate: str
    object: str
    statement_type: str
    confidence: float = 1.0
    metadata: Optional[Dict[str, Any]] = field(default_factory=dict,hash=False)
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    
    def __post_init__(self):
        """Validate statement after initialization."""
        if not 0 <= self.confidence <= 1:
            raise ValueError("Confidence must be between 0 and 1")
        
        if not all([self.subject, self.predicate, self.object]):
            raise ValueError("Subject, predicate, and object must not be empty")
    
    def format(self, style: str = "triple") -> str:
        """Format the statement as a string.
        
        Args:
            style: Formatting style ('triple', 'natural', 'symbolic')
            
        Returns:
            Formatted string representation
        """
        if style == "triple":
            return f"({self.subject}, {self.predicate}, {self.object})"
        elif style == "natural":
            return f"{self.subject} {self.predicate} {self.object}"
        elif style == "symbolic":
            return f"{self.predicate}({self.subject}, {self.object})"
        else:
            return self.format("triple")
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert statement to dictionary."""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "LogicStatement":
        """Create statement from dictionary."""
        return cls(**data)
    
    def validate(self) -> bool:
        """Validate the logic statement."""
        return all([
            isinstance(self.subject, str) and len(self.subject) > 0,
            isinstance(self.predicate, str) and len(self.predicate) > 0,
            isinstance(self.object, str) and len(self.object) > 0,
            isinstance(self.confidence, (int, float)) and 0 <= self.confidence <= 1,
            isinstance(self.statement_type, str) and len(self.statement_type) > 0
        ])
    
    def __str__(self) -> str:
        """String representation."""
        return self.format()
    
    def __repr__(self) -> str:
        """Developer representation."""
        return (f"LogicStatement(subject='{self.subject}', "
                f"predicate='{self.predicate}', object='{self.object}', "
                f"type='{self.statement_type}', confidence={self.confidence})")