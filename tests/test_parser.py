"""Tests for Parser module."""

import pytest
from synoptic_core.core.parser import Parser, Token, ParsedData


class TestParser:
    """Test cases for Parser."""
    
    def test_whitespace_tokenizer(self):
        """Test whitespace tokenization."""
        parser = Parser(tokenizer_type="whitespace")
        text = "Hello world test"
        byte_data = text.encode('utf-8')
        
        result = parser.parse(byte_data)
        
        assert isinstance(result, ParsedData)
        assert len(result.tokens) == 3
        assert result.tokens[0].value == "Hello"
        assert result.tokens[1].value == "world"
        assert result.tokens[2].value == "test"
    
    def test_punctuation_tokenizer(self):
        """Test punctuation tokenization."""
        parser = Parser(tokenizer_type="punctuation")
        text = "Hello, world!"
        byte_data = text.encode('utf-8')
        
        result = parser.parse(byte_data)
        
        tokens = [t.value for t in result.tokens]
        assert "Hello" in tokens
        assert "," in tokens
        assert "world" in tokens
        assert "!" in tokens
    
    def test_sentence_tokenizer(self):
        """Test sentence tokenization."""
        parser = Parser(tokenizer_type="sentence")
        text = "First sentence. Second sentence! Third?"
        byte_data = text.encode('utf-8')
        
        result = parser.parse(byte_data)
        
        assert len(result.tokens) == 3
        assert result.tokens[0].value == "First sentence."
        assert result.tokens[1].value == "Second sentence!"
        assert result.tokens[2].value == "Third?"
    
    def test_token_metadata(self):
        """Test token metadata extraction."""
        parser = Parser()
        text = "Test"
        byte_data = text.encode('utf-8')
        
        result = parser.parse(byte_data)
        token = result.tokens[0]
        
        assert token.byte_position == 0
        assert token.byte_length == 4
        assert token.token_type == "word"
        assert token.metadata["lowercase"] == "test"
        assert token.metadata["uppercase"] == "TEST"
    
    def test_parsed_data_metadata(self):
        """Test parsed data metadata."""
        parser = Parser()
        text = "Hello, world!"
        byte_data = text.encode('utf-8')
        
        result = parser.parse(byte_data)
        
        assert result.metadata["total_tokens"] > 0
        assert result.metadata["text_length"] == len(text)
        assert result.metadata["byte_length"] == len(byte_data)
        assert "token_types" in result.metadata
    
    def test_empty_input(self):
        """Test parsing empty input."""
        parser = Parser()
        result = parser.parse(b"")
        
        assert len(result.tokens) == 0
        assert result.metadata["total_tokens"] == 0