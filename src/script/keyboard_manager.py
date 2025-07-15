import keyboard, sys
from PySide6 import QtWidgets, QtCore

from .key import Key
from .type_def import KeyStatus, KeyStyle

keys = [
    ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P'],
    ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L'],
    ['Z', 'X', 'C', 'V', 'B', 'N', 'M']
]

class KeyboardManager(QtWidgets.QGridLayout):
    """
    Dictionary of toggled keys
        Str:KeyStatus

    Exemple: 'A':keyToChange
    """
    __toggledKeys = {}

    """
    The minimum required status to run the application
        - keyToChange
        - newKey
    """
    __nbRequiredStatus = 2

    """
    Signal emitted when a key is pressed.
    """
    keyPressed = QtCore.Signal(bool)


    def __init__(self):
        super().__init__()

        for row, key_row in enumerate(keys):
            for col, key in enumerate(key_row):
                button = Key(key)
                button.clicked.connect(lambda _, k=key: self.__onButtonClick(k))

                self.addWidget(button, row, col)


    """
    onButtonClick method is called when a key button is clicked.
    It updates the key status and refreshes the display of keys.
    It also emits a signal indicating whether the keys are correct based on the current status.
    
    Args:
        keyPressed (str): The key that was pressed.
    """
    def __onButtonClick(self, keyPressed):
        self.__updateKeyStatus(keyPressed)
        self.keyPressed.emit(self.__areKeyCorrect())
        self.__updateDisplay()



    """
    updateKeyStatus method updates the status of a key based on its current state.
    
    If the key is not in the __toggledKeys dictionary, it adds it with a status of keyToChange.
    If the key is already in the dictionary and its status is stopKey, it removes it from the dictionary.
    Otherwise, it increments the status of the key by 1.

    Args:
        keyPressed (str): The key that was pressed.
    """
    def __updateKeyStatus(self, keyPressed):
        if self.__toggledKeys.get(keyPressed) is None:
            self.__toggledKeys[keyPressed] = KeyStatus.keyToChange.value
        elif self.__toggledKeys.get(keyPressed) == 3:
            self.__toggledKeys.pop(keyPressed)
        else:
            self.__toggledKeys[keyPressed] = self.__toggledKeys.get(keyPressed) + 1


    """
    updateDisplay method updates the display of keys based on their current status.
    It iterates through all keys in the layout and applies the appropriate style based on their status.
    """
    def __updateDisplay(self):
        for i in range(self.count()):
            widget = self.itemAt(i).widget()
            if isinstance(widget, Key):
                # Reset by default and applicate the style again if necessary.
                widget.resetStatus()

                for pressedKey, status in self.__toggledKeys.items():
                    if pressedKey == widget.text():
                        for style in KeyStyle:
                            if style.name == KeyStatus(status).name:
                                widget.setStyleSheet(style.value)

    """
    areKeyCorrect method checks if the keys in __toggledKeys are valid and meet the required status.
    
    It performs the following checks:
        1. Ensures that no two keys have the same value.
        2. Checks if the key exists in the keyboard library.
        3. Counts the number of keys that have a status of keyToChange or newKey.
        4. Ensures that the number of keys with these statuses meets the minimum required status.
    
    Returns:
        bool: True if all checks pass, False otherwise.    
    """
    def __areKeyCorrect(self):
        currentRequiredStatus = 0

        for currentKey, currentValue in self.__toggledKeys.items():
            # Check if the same value is used two times
            for compareKey, compareValue in self.__toggledKeys.items():
                if currentKey is not compareKey:
                    if currentValue is compareValue:
                        return False

            status = KeyStatus(currentValue)
            if (status == KeyStatus.keyToChange
                    or status == KeyStatus.newKey):
                currentRequiredStatus = currentRequiredStatus+1

            # Check if the key exist
            try:
                keyboard.key_to_scan_codes(currentKey)
            except ValueError:
                print(f"Key '{currentKey}' is not valid.", file=sys.stderr)
                return False


        # Check if the minimum status are met
        if currentRequiredStatus < self.__nbRequiredStatus:
            return False

        # Return true if all the checks worked
        return True

    def playRebinding(self):
        print("running")