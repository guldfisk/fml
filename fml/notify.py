import requests

from pynotifier import Notification, NotificationClient
from pynotifier.backends import platform

from fml.server import MAILGUN_KEY, MAILGUN_DOMAIN, EMAIL


client = NotificationClient()
client.register_backend(platform.Backend())


def notify(
    title: str,
    description: str = "",
):
    client.notify_all(
        Notification(
            title=title,
            description=description,
            duration=5,
            urgency="normal",
        )
    )


def send_mail(
    subject: str,
    content: str,
):
    return requests.post(
        "https://api.eu.mailgun.net/v3/{}/messages".format(MAILGUN_DOMAIN),
        auth=("api", MAILGUN_KEY),
        data={
            "from": "notifications@{}".format(MAILGUN_DOMAIN),
            "to": [EMAIL],
            "subject": subject,
            "html": content,
        },
    )
