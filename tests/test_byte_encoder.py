"""Tests for ByteEncoder module."""

import pytest
from synoptic_core.core.byte_encoder import ByteEncoder


class TestByteEncoder:
    """Test cases for ByteEncoder."""
    
    def test_encode_decode(self):
        """Test basic encoding and decoding."""
        encoder = ByteEncoder()
        text = "Hello, World!"
        
        # Test encoding
        encoded = encoder.encode(text)
        assert isinstance(encoded, bytes)
        
        # Test decoding
        decoded = encoder.decode(encoded)
        assert decoded == text
    
    def test_to_byte_array(self):
        """Test conversion to byte array."""
        encoder = ByteEncoder()
        text = "ABC"
        
        byte_array = encoder.to_byte_array(text)
        assert isinstance(byte_array, list)
        assert all(isinstance(b, int) for b in byte_array)
        assert byte_array == [65, 66, 67]  # ASCII values
    
    def test_from_byte_array(self):
        """Test conversion from byte array."""
        encoder = ByteEncoder()
        byte_array = [72, 101, 108, 108, 111]  # "Hello"
        
        text = encoder.from_byte_array(byte_array)
        assert text == "Hello"
    
    def test_get_byte_patterns(self):
        """Test byte pattern extraction."""
        encoder = ByteEncoder()
        text = "ABCD"
        
        # Test bigrams (size 2)
        patterns = encoder.get_byte_patterns(text, pattern_size=2)
        assert len(patterns) == 3  # AB, BC, CD
        assert patterns[0] == (65, 66)
        assert patterns[1] == (66, 67)
        assert patterns[2] == (67, 68)
    
    def test_analyze_byte_frequency(self):
        """Test byte frequency analysis."""
        encoder = ByteEncoder()
        text = "AABBC"
        
        frequency = encoder.analyze_byte_frequency(text)
        assert frequency[65] == 2  # 'A' appears twice
        assert frequency[66] == 2  # 'B' appears twice
        assert frequency[67] == 1  # 'C' appears once
    
    def test_unicode_handling(self):
        """Test handling of Unicode characters."""
        encoder = ByteEncoder()
        text = "Hello 世界"
        
        # Should encode and decode properly
        encoded = encoder.encode(text)
        decoded = encoder.decode(encoded)
        assert decoded == text
    
    def test_empty_string(self):
        """Test handling of empty string."""
        encoder = ByteEncoder()
        
        encoded = encoder.encode("")
        assert encoded == b""
        
        decoded = encoder.decode(b"")
        assert decoded == ""