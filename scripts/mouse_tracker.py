# mouse_tracker.py
import time
from pynput import mouse
from threading import Thread

class MouseTracker:
    def __init__(self):
        self.last_move = time.time()

    def _on_move(self, x, y):
        self.last_move = time.time()

    def start_listener(self):
        listener = mouse.Listener(on_move=self._on_move)
        listener.daemon = True
        listener.start()

    def get_idle_time(self):
        """Return idle time in seconds"""
        return time.time() - self.last_move
