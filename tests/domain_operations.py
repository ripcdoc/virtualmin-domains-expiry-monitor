
import pytest
from unittest.mock import patch, Mock
from domain_operations import check_domain_expiration, check_ssl_expiration, read_domains_from_file
from exceptions import DomainFetchError, SSLCertificateError

def test_check_domain_expiration_success():
    with patch('requests.get') as mock_get:
        mock_response = Mock(status_code=200, json=lambda: {"expiration_date": "2024-12-31"})
        mock_get.return_value = mock_response

        result = check_domain_expiration("example.com")
        assert result == "2024-12-31"

def test_check_domain_expiration_failure():
    with patch('requests.get') as mock_get:
        mock_get.return_value = Mock(status_code=500)
        
        with pytest.raises(DomainFetchError):
            check_domain_expiration("example.com")

def test_check_ssl_expiration_success():
    with patch('requests.get') as mock_get:
        mock_response = Mock(status_code=200, json=lambda: {"ssl_expiration_date": "2024-12-31"})
        mock_get.return_value = mock_response

        result = check_ssl_expiration("example.com")
        assert result == "2024-12-31"

def test_read_domains_from_file(tmp_path):
    domain_file = tmp_path / "domains.txt"
    domain_file.write_text("example.com\nexample.net")
    
    with patch('config.Config.DOMAIN_FILE', str(domain_file)):
        domains = read_domains_from_file()
        assert domains == ["example.com", "example.net"]
