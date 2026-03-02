"""Project-specific exceptions."""


class ColorExError(Exception):
    """Base exception for all ColorEx failures."""


class DataValidationError(ColorExError):
    """Raised when input data cannot be parsed into a valid grid."""


class NormalizationError(ColorExError):
    """Raised when normalization mode or values are invalid."""


class RenderError(ColorExError):
    """Raised when a renderer fails to produce output."""