"""
Main file that starts the the Nice GUI server and open a window
"""

from ui.userInterface import UserInterface
from nicegui import ui

__author__ = "Dominik Kutynsky"
__copyright__ = "Copyright 2026, SETU"
__licence__ = "Open source MIT"
__version__ = "0.1.7"

if __name__ in {"__main__", "__mp_main__"}:
      UserInterface()
      ui.run(native=True, dark= True, reload=False, window_size=(1300, 800))
