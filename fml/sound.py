import os
import threading

from playsound import playsound

from fml import paths


class AlarmSoundWorker(threading.Thread):

    def run(self):
        playsound(os.path.join(paths.RESOURCE_DIRECTORY, 'alarm.wav'))


def play_sound():
    AlarmSoundWorker().start()