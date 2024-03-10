
class diffPrinter():
    _changes = []
    def __init__(self, changes) -> None:
        self.changes = changes
        pass

    @changes.setter
    def changes_setter(self, changes):
        self._changes.extend(changes)

    @changes.getter
    def changes_setter(self, changes):
        return self._changes
