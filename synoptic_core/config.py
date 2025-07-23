"""Configuration settings for Synoptic Core."""

from typing import Dict, Any
from dataclasses import dataclass, field


@dataclass
class Config:
    """Configuration container for Synoptic Core."""
    
    # Encoding settings
    default_encoding: str = "utf-8"
    byte_order: str = "little"
    
    # Parser settings
    max_token_length: int = 1024
    tokenizer_type: str = "whitespace"
    
    # Rule engine settings
    max_rule_depth: int = 10
    enable_caching: bool = True
    cache_size: int = 1000
    
    # Output settings
    default_output_format: str = "simple"
    include_metadata: bool = True
    
    # Plugin settings
    plugin_directories: list = field(default_factory=lambda: ["plugins"])
    auto_load_plugins: bool = True
    
    @classmethod
    def from_dict(cls, config_dict: Dict[str, Any]) -> "Config":
        """Create Config from dictionary."""
        return cls(**{k: v for k, v in config_dict.items() if k in cls.__annotations__})
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert Config to dictionary."""
        return {
            "default_encoding": self.default_encoding,
            "byte_order": self.byte_order,
            "max_token_length": self.max_token_length,
            "tokenizer_type": self.tokenizer_type,
            "max_rule_depth": self.max_rule_depth,
            "enable_caching": self.enable_caching,
            "cache_size": self.cache_size,
            "default_output_format": self.default_output_format,
            "include_metadata": self.include_metadata,
            "plugin_directories": self.plugin_directories,
            "auto_load_plugins": self.auto_load_plugins,
        }