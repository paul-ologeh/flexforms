import os
import logging
import configparser
from dotenv import load_dotenv
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


load_dotenv()
# CONFIG SETUP
config_path = os.path.dirname(__file__) + '/../config.ini'
config = configparser.ConfigParser()
config.read(config_path)
logger = logging.getLogger(__name__)


def expect(input, expectedType, field):
    if isinstance(input, expectedType):
        return input
    raise AssertionError("Invalid input for type", field)

def send_email(sender, recipient, message, subject):

    message = Mail(
          from_email=sender,
        to_emails=recipient,
        subject=subject,
        html_content=message)
    try:
        sendgrid_client = SendGridAPIClient(os.environ['SENDGRID_API_KEY'])
        response = sendgrid_client.send(message)
        logger.debug(response.status_code)
        logger.debug(response.body)
        logger.debug(response.headers)
        return True
    except Exception as e:
        logger.debug("Email not sent", e)
        logger.debug(e.body)
        return False