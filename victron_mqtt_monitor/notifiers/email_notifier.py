import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from loguru import logger
from jinja2 import Environment, PackageLoader

from victron_mqtt_monitor.settings import config
from victron_mqtt_monitor.notifiers.base import BaseNotifier
from victron_mqtt_monitor.interfaces import NotificationMessage


class EmailNotifier(BaseNotifier):
    """Send notifications via an SMTP server"""

    @classmethod
    def notify(cls, message: NotificationMessage) -> None:
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
    def _build_email(
        sender: str, receiver: str, message: NotificationMessage
    ) -> MIMEMultipart:
        env = Environment(
            loader=PackageLoader("victron_mqtt_monitor", "notifiers/templates")
        )

        context = message.model_dump()

        # /n doesn't work in html
        for k in context.keys():
            context[k] = context[k].replace("\n", "<br>\r\n")

        template = env.get_template("email.html")
        template = template.render(**context)

        msg = MIMEMultipart()
        msg["From"] = sender
        msg["To"] = receiver
        msg["Subject"] = f"{message.title} | Victron MQTT Monitor"
        msg.attach(MIMEText(template, "html"))

        return msg
