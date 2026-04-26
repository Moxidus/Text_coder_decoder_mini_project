from ui.userInterface import UserInterface
from nicegui import ui


if __name__ in {"__main__", "__mp_main__"}:
      UserInterface()
      ui.run(native=True, reload=False)
