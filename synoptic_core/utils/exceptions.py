"""Custom exceptions for Synoptic Core."""


class SynopticCoreError(Exception):
    """Base exception for Synoptic Core."""
    pass


class EncodingError(SynopticCoreError):
    """Raised when encoding/decoding fails."""
    pass


class ParsingError(SynopticCoreError):
    """Raised when parsing fails."""
    pass


class RuleError(SynopticCoreError):
    """Raised when rule processing fails."""
    pass


class ValidationError(SynopticCoreError):
    """Raised when validation fails."""
    pass


class PluginError(SynopticCoreError):
    """Raised when plugin operations fail."""
    pass


class ConfigurationError(SynopticCoreError):
    """Raised when configuration is invalid."""
    pass