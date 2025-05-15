import keyboard
import sys

from PySide6 import QtCore, QtWidgets, QtGui
from .type_def import PopupTypes

class MainWidget(QtWidgets.QWidget):
    isPlayButton = True

    def __init__(self):
        super().__init__()

        # Window settings
        self.setWindowTitle("Rebinder V0.2")
        self.setFixedWidth(400)  # Adjust the width as needed
        self.setFixedHeight(400)
        self.setStyleSheet("background-color: #0c0c0b;")

        # Generic widget text
        title = QtWidgets.QLabel("Rebinder", alignment=QtCore.Qt.AlignmentFlag.AlignHCenter)
        title.setFont(QtGui.QFont("Arial", 24))
        bottom = QtWidgets.QLabel("Made with ❤ by NotSkilix", alignment=QtCore.Qt.AlignmentFlag.AlignHCenter)
        bottom.setFont(QtGui.QFont("Arial", 11))

        # keyToRebind layout & elements
        keyToRebindText = QtWidgets.QLabel("Write a key to rebind (a, F3,...): ")
        self.keyToRebindField = QtWidgets.QLineEdit(maxLength=6, placeholderText="Key to rebind...")

        keyToRebinLayout = QtWidgets.QHBoxLayout()
        keyToRebinLayout.addWidget(keyToRebindText)
        keyToRebinLayout.addWidget(self.keyToRebindField)

        # NewKeyBind layout & elements
        newKeyBindText = QtWidgets.QLabel("Write the new keybind (b, F4,...): ")
        self.newKeyBindField = QtWidgets.QLineEdit(maxLength=6, placeholderText="New bind...")

        newKeyBindLayout = QtWidgets.QHBoxLayout()
        newKeyBindLayout.addWidget(newKeyBindText)
        newKeyBindLayout.addWidget(self.newKeyBindField)

        # StopRebinding layout & elements
        stopRebindingText = QtWidgets.QLabel("The keybind to stop the rebinding: ")
        self.stopRebindingKeyField = QtWidgets.QLineEdit(maxLength=6, placeholderText="Stop rebinding key...")

        stopRebindingLayout = QtWidgets.QHBoxLayout()
        stopRebindingLayout.addWidget(stopRebindingText)
        stopRebindingLayout.addWidget(self.stopRebindingKeyField)

        # Buttons
        self.playAndStopButton = QtWidgets.QPushButton("Play")

        # 'Build' the widget
        mainLayout = QtWidgets.QVBoxLayout(self)

        mainLayout.addWidget(title, alignment=QtCore.Qt.AlignmentFlag.AlignTop)
        mainLayout.addSpacing(20)
        mainLayout.addLayout(keyToRebinLayout)
        mainLayout.addSpacing(10)
        mainLayout.addLayout(newKeyBindLayout)
        mainLayout.addSpacing(10)
        mainLayout.addLayout(stopRebindingLayout)
        mainLayout.addSpacing(20)
        buttonLayout = QtWidgets.QHBoxLayout()
        buttonLayout.addWidget(self.playAndStopButton)
        mainLayout.addLayout(buttonLayout)
        mainLayout.addSpacing(30)
        mainLayout.addWidget(bottom, alignment=QtCore.Qt.AlignmentFlag.AlignBottom)

        # Add listeners
        self.playAndStopButton.clicked.connect(self.onplayAndStopButtonClick)

    """
    This function is called when the rebind button is clicked.
    
    It checks if the fields are empty and if they are not, it tries to rebind the keys.
    If the fields are empty, it raises a ValueError and prints the error message to stderr.
    """
    def onplayAndStopButtonClick(self):
        if self.isPlayButton:
            self.playRebinding()
        else:
            self.stopRebinding()

    def playRebinding(self):
        # Fields check
        try:
            # Check if the fields are empty
            if self.keyToRebindField.text() == "" and self.newKeyBindField.text() == "":
                raise ValueError("The keybinds have been left empty")
            elif self.keyToRebindField.text() == "":
                raise ValueError("The key to rebind has been left empty")
            elif self.newKeyBindField.text() == "":
                raise ValueError("The new keybind has been left empty")

            # Check if the fields are the same
            if self.keyToRebindField.text() == self.newKeyBindField.text() == self.stopRebindingKeyField.text():
                raise ValueError("Impossible to bind every keybinds to the same one")
            elif self.keyToRebindField.text() == self.newKeyBindField.text():
                raise ValueError("Impossible to rebind the old key to the itself")
            elif self.keyToRebindField.text() == self.stopRebindingKeyField.text():
                raise ValueError("Impossible to rebind the old key to the 'stop rebinding' key")
        except ValueError as e:
            self.createAndShowPopup(PopupTypes.Error,
                                    "Error on button click, one or more fields must be empty or have a the same keybind:",
                                    e)
            return

        # Rebind the keys
        self.remap = keyboard.remap_key(self.keyToRebindField.text(), self.newKeyBindField.text())

        # Set the stop rebinding key to unbind the keys
        try:
            self.stopHotkeyEvent = keyboard.hook_key(self.stopRebindingKeyField.text(), self.stopRebinding,
                                                     suppress=True)
        except ValueError as e:
            if e == "Can only normalize non-empty string names. Unexpected ''":
                self.createAndShowPopup(PopupTypes.Error,
                                        "Error on button click, the keybind to stop the rebinding is empty:", e)
                return

        self.keyToRebindField.setDisabled(True)
        self.newKeyBindField.setDisabled(True)
        self.stopRebindingKeyField.setDisabled(True)

        self.playAndStopButton.setText("Stop")
        self.isPlayButton = False

        self.window().showMinimized()
    """
    
    This function is called when the "stop rebinding" key is pressed
    
    It unbind itself and unbind the remapping (rebinding)
    Enable back the elements that were disabled before and show back the window if it is minimized
    
    Event is set to None by default because it is not required when the stop button is clicked
    """
    def stopRebinding(self, event=None):
        if hasattr(self, 'stopHotkeyEvent'):
            keyboard.unhook_key(self.stopHotkeyEvent)
            del self.stopHotkeyEvent

        try:
            keyboard.unhook(self.remap)
            del self.remap
        except Exception as e:
            print("Error while trying to unhook the keybinds: ", file=sys.stderr)
            print(e, file=sys.stderr)
            return

        self.keyToRebindField.setDisabled(False)
        self.newKeyBindField.setDisabled(False)
        self.stopRebindingKeyField.setDisabled(False)

        self.playAndStopButton.setText("Play")
        self.isPlayButton = True

        if self.window().isMinimized():
            self.window().showNormal()

    """
    This function is called when the "stop rebinding" key is pressed
    
    It creates a popup with the error message and shows it to the user
    :param type The type of popup (error, info, etc...)
    :param title The title label of the popup
    :param content The thrown error
    """
    def createAndShowPopup(self, type, title, content : ValueError):
        popup = QtWidgets.QDialog(self)

        if type == PopupTypes.Error:
            popup.setWindowTitle("Error")

        titleLabel = QtWidgets.QLabel(title)
        titleLabel.setFont(QtGui.QFont("Arial", 14))

        content = "        " + str(content)
        contentLabel = QtWidgets.QLabel(content)
        contentLabel.setFont(QtGui.QFont("Arial", 11))

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(titleLabel)
        layout.addWidget(contentLabel)

        popup.setLayout(layout)

        popup.show()