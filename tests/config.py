
import pytest
from unittest.mock import patch
from config import Config
from exceptions import ConfigError

def test_config_loading():
    with patch('os.getenv', side_effect=lambda k, d: {
        "DOMAIN_FILE": "domains.txt",
        "EMAIL_SENDER": "sender@example.com",
        "EMAIL_RECIPIENT": "recipient@example.com",
        "SMTP_SERVER": "smtp.example.com",
        "SMTP_PORT": "587",
        "SMTP_USER": "user",
        "SMTP_PASS": "pass",
        "CHECK_INTERVAL": "3600"
    }.get(k, d)):
        assert Config.DOMAIN_FILE == "domains.txt"
        assert Config.EMAIL_SENDER == "sender@example.com"

def test_invalid_config_value():
    with patch('os.getenv', side_effect=lambda k, d: "invalid"):
        with pytest.raises(ConfigError):
            int(Config.SMTP_PORT)
