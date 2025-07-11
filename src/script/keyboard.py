from PySide6 import QtCore, QtWidgets
from .key import Key

keys = [
    ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P'],
    ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L'],
    ['Z', 'X', 'C', 'V', 'B', 'N', 'M']
]

class Keyboard(QtWidgets.QGridLayout):
    def __init__(self):
        super().__init__()

        for row, key_row in enumerate(keys):
            for col, key in enumerate(key_row):
                button = Key(key)
                self.addWidget(button, row, col)