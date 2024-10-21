
import pytest
from unittest.mock import patch, Mock
from domain_monitor import notify_domain_expiration, check_domains_concurrently

def test_notify_domain_expiration():
    with patch('notifications.send_notification') as mock_send_notification:
        mock_send_notification.return_value = None
        try:
            notify_domain_expiration("domain registration", "example.com", 30)
        except Exception as e:
            pytest.fail(f"Unexpected error: {e}")

def test_check_domains_concurrently():
    with patch('domain_operations.check_domain_expiration') as mock_check_domain_expiration:
        mock_check_domain_expiration.return_value = "2024-12-31"
        domains = ["example.com", "example.net"]
        
        try:
            check_domains_concurrently(domains)
        except Exception as e:
            pytest.fail(f"Unexpected error: {e}")
