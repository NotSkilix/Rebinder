from PySide6 import QtWidgets
from .key import Key
from .type_def import KeyStatus, KeyStyle

keys = [
    ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P'],
    ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L'],
    ['Z', 'X', 'C', 'V', 'B', 'N', 'M']
]

class Keyboard(QtWidgets.QGridLayout):
    """
    Dictionary of toggled keys
        Str:KeyStatus

    Exemple: 'A':keyToChange
    """
    toggledKeys = {}

    def __init__(self):
        super().__init__()

        for row, key_row in enumerate(keys):
            for col, key in enumerate(key_row):
                button = Key(key)
                button.clicked.connect(lambda _, k=key: self.onButtonClick(k))

                self.addWidget(button, row, col)


    """
    onButtonClick method is called when a key button is clicked.
    It updates the key status and refreshes the display of keys.
    
    Args:
        keyPressed (str): The key that was pressed.
    """
    def onButtonClick(self, keyPressed):
        self.updateKeyStatus(keyPressed)
        self.updateDisplay()


    """
    updateKeyStatus method updates the status of a key based on its current state.
    
    If the key is not in the toggledKeys dictionary, it adds it with a status of keyToChange.
    If the key is already in the dictionary and its status is stopKey, it removes it from the dictionary.
    Otherwise, it increments the status of the key by 1.

    Args:
        keyPressed (str): The key that was pressed.
    """
    def updateKeyStatus(self, keyPressed):
        if self.toggledKeys.get(keyPressed) is None:
            self.toggledKeys[keyPressed] = KeyStatus.keyToChange.value
        elif self.toggledKeys.get(keyPressed) == 3:
            self.toggledKeys.pop(keyPressed)
        else:
            self.toggledKeys[keyPressed] = self.toggledKeys.get(keyPressed) + 1

        print(self.toggledKeys)

    """
    updateDisplay method updates the display of keys based on their current status.
    It iterates through all keys in the layout and applies the appropriate style based on their status.
    """
    def updateDisplay(self):
        for i in range(self.count()):
            widget = self.itemAt(i).widget()
            if isinstance(widget, Key):
                # Reset by default and applicate the style again if necessary.
                widget.resetStatus()

                for pressedKey, status in self.toggledKeys.items():
                    if pressedKey == widget.text():
                        for style in KeyStyle:
                            if style.name == KeyStatus(status).name:
                                widget.setStyleSheet(style.value)