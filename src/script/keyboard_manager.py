import keyboard
import sys
import json
from PySide6 import QtWidgets, QtCore

from src.script.key import Key
from src.types.type_def import KeyStatus, KeyStyle, KeySize, KEYBOARD_LAYOUT_PATH

KEYBOARD_TYPE = "QWERTY"
KEYBOARD_SIZE = "FULL"
KEYBOARD_LIST_NAME = "keyboards"

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

    """
    Signal emitted when the stop key is pressed.
    """
    stopKeyPressed = QtCore.Signal()

    """
    Constructor for KeyboardManager.
    """
    def __init__(self):
        super().__init__()

        # Read the KEYBOARD_LAYOUT_PATH.json for the first keyboard layout
        with open(KEYBOARD_LAYOUT_PATH) as file:
            jsonObject = json.load(file)
            if jsonObject[KEYBOARD_LIST_NAME]:
                keyboardList = jsonObject[KEYBOARD_LIST_NAME]
                firstKeyboard = keyboardList[0] # Select the first keyboard for now
                if firstKeyboard["type"] == KEYBOARD_TYPE:
                    keyboardLayout = firstKeyboard["layout"]
                    for row in range(len(keyboardLayout)):
                        col=0
                        for j in keyboardLayout[row]:
                            key = j["key"]
                            size = j["size"]


                            if key != "":
                                button = Key(key, keySize=KeySize[size])
                                button.clicked.connect(lambda _, k=key: self.__onButtonClick(k))
                            else:
                                col+=1

                            self.addWidget(button, row, col)
                            col+=1


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
            self.__toggledKeys[keyPressed] = KeyStatus.KEY_TO_CHANGE.value
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
                                widget.setStyleSheet(style)

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
            if (status == KeyStatus.KEY_TO_CHANGE
                    or status == KeyStatus.NEW_KEY):
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

    """
    playRebinding method starts the rebinding process by getting the keys to change, new key, and stop key.
    
    It then remaps the keys and binds the stop key to stop the rebinding process.
    Also disables the keys from being pressed during the rebinding process.
    
    Raises:
        Exception: If the remapping or binding fails.
    """
    def playRebinding(self):
        # Get the keys
        toChangeKey = None
        newKey = None
        stopKey = None

        for key, value in self.__toggledKeys.items():
            value = KeyStatus(value)
            if value == KeyStatus.KEY_TO_CHANGE:
                toChangeKey = key
            elif value == KeyStatus.NEW_KEY:
                newKey = key
            elif value == KeyStatus.STOP_KEY:
                stopKey = key
            else:
                print(f"Key '{key}' has an invalid status: {value.name}", file=sys.stderr)

        # Rebind the two main keys (Throws an exception on failure)
        self.remap = keyboard.remap_key(toChangeKey, newKey)

        # Bind the stop key (Throws an exception on failure)
        if stopKey is not None:
            self.stopHotkeyEvent = keyboard.hook_key(stopKey, self.__emitStopKeySignal, True)

        # Disable the keys from being pressed
        self.__disableKeys(True)

    """
    emitStopKeySignal method emits the stopKeyPressed signal.
    """
    def __emitStopKeySignal(self, event=None):
        self.stopKeyPressed.emit()

    """
    stopRebinding method stops the rebinding process by unhooking the play/stop key and the remapped keys.
    
    It also enables the keys back in the keyboard layout.
    
    Args:
        event (optional): The event that triggered the stop rebinding. Defaults to None.
    """
    def stopRebinding(self):
        # Enable the keys back
        self.__disableKeys(False)

        # Unhook the play/stop key
        if hasattr(self, 'stopHotkeyEvent'):
            keyboard.unhook_key(self.stopHotkeyEvent)
            del self.stopHotkeyEvent


        # Unhook the keybinds
        if hasattr(self, 'remap'):
            keyboard.unhook(self.remap)
            del self.remap

    """
    disableKeys method disables or enables all keys in the keyboard layout.
    
    Args:
        value (bool): If True, disables the keys; if False, enables them.
    """
    def __disableKeys(self, value : bool):
        for i in range(self.count()):
            widget = self.itemAt(i).widget()
            if isinstance(widget, Key):
                widget.setDisabled(value)