"""Parser for tokenizing and structuring byte-encoded data."""

from typing import List, Dict, Any, Union
from dataclasses import dataclass
import re


@dataclass
class Token:
    """Represents a parsed token."""
    value: str
    byte_position: int
    byte_length: int
    token_type: str
    metadata: Dict[str, Any] = None


@dataclass
class ParsedData:
    """Container for parsed data."""
    tokens: List[Token]
    byte_data: bytes
    metadata: Dict[str, Any]


class Parser:
    """Tokenizes and structures byte-encoded input."""
    
    def __init__(self, tokenizer_type: str = "whitespace"):
        """Initialize Parser.
        
        Args:
            tokenizer_type: Type of tokenizer to use
        """
        self.tokenizer_type = tokenizer_type
        self.tokenizers = {
            "whitespace": self._tokenize_whitespace,
            "punctuation": self._tokenize_punctuation,
            "sentence": self._tokenize_sentence,
        }
        
    def parse(self, byte_data: bytes) -> ParsedData:
        """Parse byte data into structured format.
        
        Args:
            byte_data: Input bytes
            
        Returns:
            ParsedData object containing tokens and metadata
        """
        # Decode to text for tokenization
        text = byte_data.decode('utf-8')
        
        # Tokenize based on selected tokenizer
        tokenizer = self.tokenizers.get(self.tokenizer_type, self._tokenize_whitespace)
        tokens = tokenizer(text, byte_data)
        
        # Extract metadata
        metadata = self._extract_metadata(text, tokens)
        
        return ParsedData(
            tokens=tokens,
            byte_data=byte_data,
            metadata=metadata
        )
    
    def _tokenize_whitespace(self, text: str, byte_data: bytes) -> List[Token]:
        """Tokenize by whitespace."""
        tokens = []
        byte_position = 0
        
        for word in text.split():
            # Find byte position
            word_bytes = word.encode('utf-8')
            byte_index = byte_data.find(word_bytes, byte_position)
            
            if byte_index != -1:
                token = Token(
                    value=word,
                    byte_position=byte_index,
                    byte_length=len(word_bytes),
                    token_type="word",
                    metadata={"lowercase": word.lower(), "uppercase": word.upper()}
                )
                tokens.append(token)
                byte_position = byte_index + len(word_bytes)
        
        return tokens
    
    def _tokenize_punctuation(self, text: str, byte_data: bytes) -> List[Token]:
        """Tokenize including punctuation."""
        pattern = r'\b\w+\b|[^\w\s]'
        tokens = []
        
        for match in re.finditer(pattern, text):
            word = match.group()
            word_bytes = word.encode('utf-8')
            byte_index = byte_data.find(word_bytes, match.start())
            
            token_type = "punctuation" if not word.isalnum() else "word"
            
            token = Token(
                value=word,
                byte_position=byte_index,
                byte_length=len(word_bytes),
                token_type=token_type
            )
            tokens.append(token)
        
        return tokens
    
    def _tokenize_sentence(self, text: str, byte_data: bytes) -> List[Token]:
        """Tokenize by sentences."""
        sentence_pattern = r'[.!?]+\s*'
        tokens = []
        start = 0
        
        for match in re.finditer(sentence_pattern, text):
            end = match.end()
            sentence = text[start:end].strip()
            
            if sentence:
                sentence_bytes = sentence.encode('utf-8')
                byte_index = byte_data.find(sentence_bytes, start)
                
                token = Token(
                    value=sentence,
                    byte_position=byte_index,
                    byte_length=len(sentence_bytes),
                    token_type="sentence"
                )
                tokens.append(token)
            
            start = end
        
        # Handle last sentence without ending punctuation
        if start < len(text):
            sentence = text[start:].strip()
            if sentence:
                sentence_bytes = sentence.encode('utf-8')
                byte_index = byte_data.find(sentence_bytes, start)
                
                token = Token(
                    value=sentence,
                    byte_position=byte_index,
                    byte_length=len(sentence_bytes),
                    token_type="sentence"
                )
                tokens.append(token)
        
        return tokens
    
    def _extract_metadata(self, text: str, tokens: List[Token]) -> Dict[str, Any]:
        """Extract metadata from parsed data."""
        return {
            "total_tokens": len(tokens),
            "text_length": len(text),
            "byte_length": len(text.encode('utf-8')),
            "token_types": self._count_token_types(tokens),
            "has_punctuation": any(t.token_type == "punctuation" for t in tokens),
        }
    
    def _count_token_types(self, tokens: List[Token]) -> Dict[str, int]:
        """Count occurrences of each token type."""
        type_counts = {}
        for token in tokens:
            type_counts[token.token_type] = type_counts.get(token.token_type, 0) + 1
        return type_counts