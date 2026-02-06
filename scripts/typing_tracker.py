# typing_tracker.py
import time
from pynput import keyboard
from threading import Thread

class TypingTracker:
    def __init__(self, window=60):
        self.key_times = []  # timestamps of key presses
        self.window = window  # seconds for sliding window

    def _on_press(self, key):
        self.key_times.append(time.time())

    def start_listener(self):
        listener = keyboard.Listener(on_press=self._on_press)
        listener.daemon = True
        listener.start()

    def get_typing_speed(self):
        """Return characters per minute (CPM) over the sliding window"""
        now = time.time()
        self.key_times = [t for t in self.key_times if t > now - self.window]
        cpm = len(self.key_times) * (60 / self.window)  # CPM
        return cpm



