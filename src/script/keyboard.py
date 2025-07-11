from PySide6 import QtWidgets
from .key import Key

keys = [
    ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P'],
    ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L'],
    ['Z', 'X', 'C', 'V', 'B', 'N', 'M']
]

class Keyboard(QtWidgets.QGridLayout):
    toggledKeys = []

    def __init__(self):
        super().__init__()

        for row, key_row in enumerate(keys):
            for col, key in enumerate(key_row):
                button = Key(key)
                button.clicked.connect(lambda _, k=key: self.onButtonClick(k))

                self.addWidget(button, row, col)


    def onButtonClick(self, key):
        if self.isKeyAlreadyToggled(key):
            self.toggledKeys.remove(key)
        else:
            self.toggledKeys.append(key)

        self.updateKeysStatus()

    """
    Checks if a key is already toggled.
    
    Args:
        key (str): The key to check.
    Returns:
        bool: True if the key is already toggled, False otherwise.
    """
    def isKeyAlreadyToggled(self, key):
        for toggledKey in self.toggledKeys:
            if toggledKey == key:
                return True
        return False

    def updateKeysStatus(self):
        for i in range(self.count()):
            widget = self.itemAt(i).widget()
            if isinstance(widget, Key):
                # Reset by default and applicate the style again if necessary.
                widget.resetStatus()

                for toggledKey in self.toggledKeys:
                    if widget.text() == toggledKey:
                        widget.setStyleSheet("""
                                            background-color: cyan
                                            """)