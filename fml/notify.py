import os
import threading
import requests

from playsound import playsound
from pynotifier import Notification

from fml import MAILGUN_KEY, MAILGUN_DOMAIN, EMAIL, paths


class AlarmSoundWorker(threading.Thread):

    def run(self):
        playsound(os.path.join(paths.RESOURCE_DIRECTORY, 'alarm.wav'))


def play_sound():
    AlarmSoundWorker().start()


def notify(
    title: str,
    description: str = '',
):
    Notification(
        title = title,
        description = description,
        duration = 5,
        urgency = Notification.URGENCY_NORMAL,
    ).send()


def send_mail(
    subject: str,
    content: str,
):
    return requests.post(
        "https://api.eu.mailgun.net/v3/{}/messages".format(MAILGUN_DOMAIN),
        auth = ("api", MAILGUN_KEY),
        data = {
            "from": "notifications@{}".format(MAILGUN_DOMAIN),
            "to": [EMAIL],
            "subject": subject,
            "html": content,
        },
    )
