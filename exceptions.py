# finaTSE/exceptions.py

class FinaTSError(Exception):
    """Base exception for finaTSE."""
    pass

class SymbolNotFoundError(FinaTSError):
    """Raised when a symbol is not found on TSETMC."""
    pass

class NetworkError(FinaTSError):
    """Raised when there's a network or HTTP error."""
    pass
