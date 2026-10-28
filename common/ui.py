"""Small Tkinter helpers shared by the desktop screens."""


class Debouncer:
    """Run a callback only after typing has paused for a moment."""

    def __init__(self, widget, delay=250):
        self.widget = widget
        self.delay = delay
        self._job = None

    def call(self, callback):
        if self._job is not None:
            self.widget.after_cancel(self._job)
        self._job = self.widget.after(self.delay, callback)
