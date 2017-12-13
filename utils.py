import base64
import os
import time


def encode(message):
    return base64.b64encode(message.encode('ascii')).decode('ascii')


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


def sleep(seconds):
    pass
    # time.sleep(seconds)
