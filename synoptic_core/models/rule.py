"""Rule model for pattern matching."""

from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field, asdict
import re


@dataclass(unsafe_hash=True)
class Rule:
    """Represents a pattern-matching rule."""
    
    name: str
    pattern: str
    rule_type: str  # 'regex', 'token', 'sequence', 'custom'
    action: Dict[str, Any] - field(hash-false)
    description: str = ""
    priority: int = 50
    enabled: bool = True
    metadata: Optional[Dict[str, Any]] = field(default_factory=dict, hash=False)
    
    def __post_init__(self):
        """Validate rule after initialization."""
        if self.rule_type not in ['regex', 'token', 'sequence', 'custom']:
            raise ValueError(f"Invalid rule type: {self.rule_type}")
        
        if self.rule_type == 'regex':
            try:
                re.compile(self.pattern)
            except re.error as e:
                raise ValueError(f"Invalid regex pattern: {e}")
        
        if not 0 <= self.priority <= 100:
            raise ValueError("Priority must be between 0 and 100")
    
    def matches(self, text: str) -> bool:
        """Check if the rule matches the given text.
        
        Args:
            text: Input text to match against
            
        Returns:
            True if rule matches, False otherwise
        """
        if not self.enabled:
            return False
        
        if self.rule_type == 'regex':
            return bool(re.search(self.pattern, text, re.IGNORECASE))
        elif self.rule_type == 'token':
            tokens = text.lower().split()
            pattern_tokens = self.pattern.lower().split()
            return any(token in tokens for token in pattern_tokens)
        elif self.rule_type == 'sequence':
            return self.pattern.lower() in text.lower()
        else:
            return False
    
    def extract_matches(self, text: str) -> List[Dict[str, Any]]:
        """Extract all matches from text.
        
        Args:
            text: Input text to extract from
            
        Returns:
            List of match dictionaries
        """
        matches = []
        
        if self.rule_type == 'regex':
            for match in re.finditer(self.pattern, text, re.IGNORECASE):
                match_dict = {
                    'full_match': match.group(0),
                    'groups': match.groups(),
                    'start': match.start(),
                    'end': match.end()
                }
                matches.append(match_dict)
        
        elif self.rule_type == 'token':
            tokens = text.split()
            pattern_tokens = self.pattern.split()
            for i, token in enumerate(tokens):
                if token.lower() in [p.lower() for p in pattern_tokens]:
                    matches.append({
                        'token': token,
                        'position': i,
                        'matched_pattern': self.pattern
                    })
        
        return matches
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert rule to dictionary."""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Rule":
        """Create rule from dictionary."""
        return cls(**data)
    
    def __str__(self) -> str:
        """String representation."""
        return f"Rule('{self.name}': {self.rule_type} pattern '{self.pattern}')"
    
    def __repr__(self) -> str:
        """Developer representation."""
        return (f"Rule(name='{self.name}', pattern='{self.pattern}', "
                f"type='{self.rule_type}', priority={self.priority})")