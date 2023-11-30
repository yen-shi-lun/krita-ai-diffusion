from enum import Enum
from ai_diffusion.properties import Property, PropertyMeta
from PyQt5.QtCore import QObject, pyqtBoundSignal, pyqtSignal


class Piong(Enum):
    a = 1
    b = 2


class ObjectWithProperties(QObject, metaclass=PropertyMeta):
    inty = Property(0)
    stringy = Property("")
    enumy = Property(Piong.a)
    custom = Property(3, getter="get_custom", setter="set_custom")

    inty_changed = pyqtSignal(int)
    stringy_changed = pyqtSignal(str)
    enumy_changed = pyqtSignal(Piong)
    custom_changed = pyqtSignal(int)

    def __init__(self):
        super().__init__()

    def get_custom(self):
        return self._custom + 10

    def set_custom(self, value: int):
        self._custom = value + 1
        self.custom_changed.emit(self._custom)


def test_property():
    called = []

    def callback(x):
        called.append(x)

    t = ObjectWithProperties()
    t.inty_changed.connect(callback)
    t.inty = 42
    assert t.inty == 42

    t.stringy_changed.connect(callback)
    t.stringy = "hello"
    assert t.stringy == "hello"

    t.enumy_changed.connect(callback)
    t.enumy = Piong.b
    assert t.enumy == Piong.b

    assert t.custom == 13
    t.custom_changed.connect(callback)
    t.custom = 4
    assert t.custom == 15

    assert called == [42, "hello", Piong.b, 5]
