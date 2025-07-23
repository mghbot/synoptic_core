"""Byte-level encoder for text processing."""

from typing import List, Union, Tuple
import struct


class ByteEncoder:
    """Handles byte-level encoding and decoding of text."""
    
    def __init__(self, encoding: str = "utf-8", byte_order: str = "little"):
        """Initialize ByteEncoder.
        
        Args:
            encoding: Text encoding to use
            byte_order: Byte order ('little' or 'big')
        """
        self.encoding = encoding
        self.byte_order = byte_order
        
    def encode(self, text: str) -> bytes:
        """Encode text to bytes.
        
        Args:
            text: Input text string
            
        Returns:
            Byte representation of the text
        """
        return text.encode(self.encoding)
    
    def decode(self, byte_data: bytes) -> str:
        """Decode bytes to text.
        
        Args:
            byte_data: Input bytes
            
        Returns:
            Decoded text string
        """
        return byte_data.decode(self.encoding)
    
    def to_byte_array(self, text: str) -> List[int]:
        """Convert text to array of byte values.
        
        Args:
            text: Input text
            
        Returns:
            List of integer byte values
        """
        byte_data = self.encode(text)
        return list(byte_data)
    
    def from_byte_array(self, byte_array: List[int]) -> str:
        """Convert byte array to text.
        
        Args:
            byte_array: List of integer byte values
            
        Returns:
            Decoded text string
        """
        byte_data = bytes(byte_array)
        return self.decode(byte_data)
    
    def get_byte_patterns(self, text: str, pattern_size: int = 2) -> List[Tuple[int, ...]]:
        """Extract byte patterns of specified size.
        
        Args:
            text: Input text
            pattern_size: Size of byte patterns to extract
            
        Returns:
            List of byte pattern tuples
        """
        byte_array = self.to_byte_array(text)
        patterns = []
        
        for i in range(len(byte_array) - pattern_size + 1):
            pattern = tuple(byte_array[i:i + pattern_size])
            patterns.append(pattern)
        
        return patterns
    
    def analyze_byte_frequency(self, text: str) -> dict:
        """Analyze frequency of bytes in text.
        
        Args:
            text: Input text
            
        Returns:
            Dictionary mapping byte values to their frequencies
        """
        byte_array = self.to_byte_array(text)
        frequency = {}
        
        for byte_val in byte_array:
            frequency[byte_val] = frequency.get(byte_val, 0) + 1
        
        return frequency