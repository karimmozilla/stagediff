
class diffPrinter():
    _changes = []
    def __init__(self) -> None:
        pass

    @property
    def changes(self):
        return self._changes

    @changes.setter
    def changes(self, value):
        self._changes.extend(value)

