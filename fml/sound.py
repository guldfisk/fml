import os
import threading

from playsound import playsound

from fml import paths


class AlarmSoundWorker(threading.Thread):
    def run(self):
        ding()


def ding():
    playsound(os.path.join(paths.RESOURCE_DIRECTORY, "alarm.wav"))


def ding_sync():
    AlarmSoundWorker().start()
