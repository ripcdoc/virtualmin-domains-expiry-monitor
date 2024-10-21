
import pytest
from unittest.mock import patch, Mock
from notifications import send_notification, render_email_template
from exceptions import NotificationError

def test_render_email_template_success():
    with patch('jinja2.Environment.get_template') as mock_get_template:
        mock_template = Mock(render=lambda context: "Rendered Content")
        mock_get_template.return_value = mock_template

        result = render_email_template("email_html.j2", {"subject": "Test"})
        assert result == "Rendered Content"

def test_send_notification_success():
    with patch('smtplib.SMTP') as mock_smtp:
        mock_smtp.return_value.sendmail = Mock()
        
        try:
            send_notification("Test Subject", "HTML Content", "Plain Content")
        except NotificationError:
            pytest.fail("NotificationError raised unexpectedly!")

def test_send_notification_failure():
    with patch('smtplib.SMTP', side_effect=Exception("SMTP Error")):
        with pytest.raises(NotificationError):
            send_notification("Test Subject", "HTML Content", "Plain Content")
