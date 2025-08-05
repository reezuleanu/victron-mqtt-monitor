import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from loguru import logger

from victron_mqtt_monitor.settings import config
from victron_mqtt_monitor.notifiers.base import BaseNotifier


class EmailNotifier(BaseNotifier):
    """Send notifications via an SMTP server"""

    @classmethod
    def notify(cls, message: str) -> None:
        """Notify all users set in config.EMAIL_RECIPIENTS

        Args:
            message (str): The body of the email
        """

        for receiver_email in config.EMAIL_RECIPIENTS:

            msg = cls._build_email(config.SMTP_EMAIL, receiver_email, message)

            try:
                server = smtplib.SMTP(config.SMTP_SERVER, config.SMTP_PORT)
                server.starttls()
                server.login(config.SMTP_EMAIL, config.SMTP_PASSWORD)
                server.sendmail(config.SMTP_EMAIL, receiver_email, msg.as_string())
                logger.info(f"Email sent to {receiver_email} successfully!")
            except Exception as e:
                logger.exception(f"Error sending email to {receiver_email}: {e}")
            finally:
                server.quit()

    @staticmethod
    def _build_email(sender, receiver, message) -> MIMEMultipart:
        msg = MIMEMultipart()
        msg["From"] = sender
        msg["To"] = receiver
        msg["Subject"] = "Victron MQTT Monitor"
        msg.attach(MIMEText(message, "plain"))

        return msg
