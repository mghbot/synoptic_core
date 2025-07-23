"""Rule engine for applying pattern-matching rules."""

from typing import List, Optional, Dict, Any
import re
from functools import lru_cache

from synoptic_core.models.rule import Rule
from synoptic_core.models.logic_statement import LogicStatement
from synoptic_core.core.parser import ParsedData, Token


class RuleEngine:
    """Applies pattern-matching rules to parsed data."""
    
    def __init__(self, enable_caching: bool = True, cache_size: int = 1000):
        """Initialize RuleEngine.
        
        Args:
            enable_caching: Whether to enable rule caching
            cache_size: Maximum cache size
        """
        self.enable_caching = enable_caching
        self.cache_size = cache_size
        self.builtin_rules = self._initialize_builtin_rules()
        
        if enable_caching:
            self._apply_single_rule = lru_cache(maxsize=cache_size)(self._apply_single_rule)
    
    def apply_rules(self, parsed_data: ParsedData, custom_rules: Optional[List[Rule]] = None) -> List[LogicStatement]:
        """Apply rules to parsed data and generate logic statements.
        
        Args:
            parsed_data: Parsed input data
            custom_rules: Optional custom rules to apply
            
        Returns:
            List of generated logic statements
        """
        rules = custom_rules if custom_rules else self.builtin_rules
        statements = []
        
        for rule in rules:
            rule_statements = self._apply_single_rule(rule, parsed_data)
            statements.extend(rule_statements)
        
        # Post-process statements
        statements = self._merge_duplicate_statements(statements)
        statements = self._calculate_confidence_scores(statements)
        
        return statements
    
    def _apply_single_rule(self, rule: Rule, parsed_data: ParsedData) -> List[LogicStatement]:
        """Apply a single rule to parsed data."""
        statements = []
        
        # Convert tokens to searchable text
        text_representation = " ".join(token.value for token in parsed_data.tokens)
        
        # Apply pattern matching
        if rule.rule_type == "regex":
            matches = re.finditer(rule.pattern, text_representation, re.IGNORECASE)
            for match in matches:
                statement = self._create_statement_from_match(rule, match, parsed_data)
                if statement:
                    statements.append(statement)
        
        elif rule.rule_type == "token":
            statements.extend(self._apply_token_rule(rule, parsed_data))
        
        elif rule.rule_type == "sequence":
            statements.extend(self._apply_sequence_rule(rule, parsed_data))
        
        return statements
    
    def _apply_token_rule(self, rule: Rule, parsed_data: ParsedData) -> List[LogicStatement]:
        """Apply token-based rule."""
        statements = []
        pattern_tokens = rule.pattern.split()
        
        for i, token in enumerate(parsed_data.tokens):
            if token.value.lower() in [p.lower() for p in pattern_tokens]:
                # Look for context around the token
                context = self._get_token_context(parsed_data.tokens, i, window=2)
                
                statement = LogicStatement(
                    subject=token.value,
                    predicate=rule.action.get("predicate", "matches"),
                    object=rule.action.get("object", "pattern"),
                    statement_type=rule.action.get("statement_type", "assertion"),
                    confidence=0.8,
                    metadata={
                        "rule": rule.name,
                        "context": context,
                        "token_position": i
                    }
                )
                statements.append(statement)
        
        return statements
    
    def _apply_sequence_rule(self, rule: Rule, parsed_data: ParsedData) -> List[LogicStatement]:
        """Apply sequence-based rule."""
        statements = []
        sequence = rule.pattern.split()
        tokens = [t.value.lower() for t in parsed_data.tokens]
        
        # Find sequences
        for i in range(len(tokens) - len(sequence) + 1):
            if tokens[i:i+len(sequence)] == [s.lower() for s in sequence]:
                # Extract subject, predicate, object from sequence
                statement = LogicStatement(
                    subject=parsed_data.tokens[i].value,
                    predicate=rule.action.get("predicate", "relates_to"),
                    object=parsed_data.tokens[i+len(sequence)-1].value if len(sequence) > 1 else "self",
                    statement_type=rule.action.get("statement_type", "relation"),
                    confidence=0.9,
                    metadata={
                        "rule": rule.name,
                        "sequence_start": i,
                        "sequence_length": len(sequence)
                    }
                )
                statements.append(statement)
        
        return statements
    
    def _create_statement_from_match(self, rule: Rule, match, parsed_data: ParsedData) -> Optional[LogicStatement]:
        """Create logic statement from regex match."""
        try:
            groups = match.groups()
            
            # Extract components based on rule action
            subject = groups[0] if groups else match.group(0)
            predicate = rule.action.get("predicate", "matches")
            obj = groups[1] if len(groups) > 1 else rule.action.get("object", "pattern")
            
            return LogicStatement(
                subject=subject,
                predicate=predicate,
                object=obj,
                statement_type=rule.action.get("statement_type", "extraction"),
                confidence=0.7,
                metadata={
                    "rule": rule.name,
                    "match_position": match.start(),
                    "match_text": match.group(0)
                }
            )
        except Exception:
            return None
    
    def _get_token_context(self, tokens: List[Token], index: int, window: int) -> List[str]:
        """Get context tokens around a specific index."""
        start = max(0, index - window)
        end = min(len(tokens), index + window + 1)
        return [t.value for t in tokens[start:end]]
    
    def _merge_duplicate_statements(self, statements: List[LogicStatement]) -> List[LogicStatement]:
        """Merge duplicate statements, keeping highest confidence."""
        unique_statements = {}
        
        for stmt in statements:
            key = (stmt.subject, stmt.predicate, stmt.object)
            if key not in unique_statements or stmt.confidence > unique_statements[key].confidence:
                unique_statements[key] = stmt
        
        return list(unique_statements.values())
    
    def _calculate_confidence_scores(self, statements: List[LogicStatement]) -> List[LogicStatement]:
        """Recalculate confidence scores based on statement relationships."""
        # Simple confidence adjustment based on supporting statements
        for i, stmt in enumerate(statements):
            supporting_count = sum(
                1 for other in statements 
                if other != stmt and (
                    other.subject == stmt.subject or 
                    other.object == stmt.object
                )
            )
            
            # Boost confidence if supported by other statements
            if supporting_count > 0:
                stmt.confidence = min(1.0, stmt.confidence + (0.05 * supporting_count))
        
        return statements
    
    def _initialize_builtin_rules(self) -> List[Rule]:
        """Initialize built-in rules."""
        return [
            Rule(
                name="is_a_relation",
                pattern=r"(\w+)\s+is\s+(?:a|an)\s+(\w+)",
                rule_type="regex",
                action={
                    "predicate": "is_a",
                    "statement_type": "classification"
                },
                description="Detects 'X is a Y' relationships"
            ),
            Rule(
                name="has_relation",
                pattern=r"(\w+)\s+has\s+(\w+)",
                rule_type="regex",
                action={
                    "predicate": "has",
                    "statement_type": "property"
                },
                description="Detects 'X has Y' relationships"
            ),
            Rule(
                name="action_object",
                pattern=r"(\w+)\s+(\w+s)\s+(\w+)",
                rule_type="regex",
                action={
                    "predicate": "acts_on",
                    "statement_type": "action"
                },
                description="Detects subject-verb-object patterns"
            ),
            Rule(
                name="if_then",
                pattern="if then",
                rule_type="sequence",
                action={
                    "predicate": "implies",
                    "statement_type": "conditional"
                },
                description="Detects conditional statements"
            ),
            Rule(
                name="definition",
                pattern=r"(\w+)\s+is\s+defined\s+as\s+(.+)",
                rule_type="regex",
                action={
                    "predicate": "defined_as",
                    "statement_type": "definition"
                },
                description="Detects definitions"
            ),
        ]
    
    def get_builtin_rules(self) -> List[Rule]:
        """Get list of built-in rules."""
        return self.builtin_rules
    
    def add_rule(self, rule: Rule):
        """Add a custom rule to the engine."""
        self.builtin_rules.append(rule)