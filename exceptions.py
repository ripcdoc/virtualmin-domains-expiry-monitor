
class DomainMonitorError(Exception):
    """Base exception for domain monitor script."""
    pass

class DomainFetchError(DomainMonitorError):
    """Raised when there is an issue fetching domain data."""
    pass

class SSLCertificateError(DomainMonitorError):
    """Raised when there is an issue with SSL certificate checks."""
    pass

class NotificationError(DomainMonitorError):
    """Raised when there is an issue sending notifications."""
    pass

class ConfigError(DomainMonitorError):
    """Raised when there is an issue with configuration loading."""
    pass
