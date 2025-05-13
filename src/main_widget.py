import keyboard
import sys

from PySide6 import QtCore, QtWidgets, QtGui
from type_def import PopupTypes

class MainWidget(QtWidgets.QWidget):
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
        self.stopRebindingKey = QtWidgets.QLineEdit(maxLength=6, placeholderText="Stop rebinding key...")

        stopRebindingLayout = QtWidgets.QHBoxLayout()
        stopRebindingLayout.addWidget(stopRebindingText)
        stopRebindingLayout.addWidget(self.stopRebindingKey)

        # Buttons
        self.rebindButton = QtWidgets.QPushButton("Rebind")
        self.stopRebindButton = QtWidgets.QPushButton("Stop")
        self.stopRebindButton.setDisabled(True)

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
        buttonLayout.addWidget(self.rebindButton)
        buttonLayout.addWidget(self.stopRebindButton)
        mainLayout.addLayout(buttonLayout)
        mainLayout.addSpacing(30)
        mainLayout.addWidget(bottom, alignment=QtCore.Qt.AlignmentFlag.AlignBottom)

        # Add listeners
        self.rebindButton.clicked.connect(self.onRebindButtonClick)

    """
    This function is called when the rebind button is clicked.
    
    It checks if the fields are empty and if they are not, it tries to rebind the keys.
    If the fields are empty, it raises a ValueError and prints the error message to stderr.
    """
    def onRebindButtonClick(self):
        try:
            if self.newKeyBindField.text() == "" and self.keyToRebindField.text() == "":
                raise ValueError("Both fields must contain a value in order to rebind the keys")
            elif self.newKeyBindField.text() == "":
                raise ValueError("The new keybind field must not be empty when rebinding")
            elif self.keyToRebindField.text() == "":
                raise ValueError("The key to rebind must not be empty when rebinding")

            if self.newKeyBindField.text() ==  self.keyToRebindField.text():
                raise ValueError("You can't rebind a key to itself")
            elif self.keyToRebindField.text() == self.stopRebindingKey.text():
                raise ValueError("It is not possible to bind the 'stop rebinding' key to the rebinded key")
        except ValueError as e:
            self.createAndShowPopup(PopupTypes.Error, "Error on button click, one or more fields must be empty or have a the same keybind:",e)
            return

        try:
            self.remap = keyboard.remap_key(self.keyToRebindField.text(), self.newKeyBindField.text())
        except ValueError as e:
            self.createAndShowPopup(PopupTypes.Error, "Error on button click, one of the keybind must be incorrect/inexistant:",e)
            return

        self.keyToRebindField.setDisabled(True)
        self.newKeyBindField.setDisabled(True)
        self.stopRebindingKey.setDisabled(True)
        self.rebindButton.setDisabled(True)

        try:
            self.stopHotkeyEvent = keyboard.hook_key(self.stopRebindingKey.text(),self.unbindKeys, suppress=True)
        except ValueError as e:
            print("Error on button click, the keybind to stop the rebinding doesn't exist: ",  file=sys.stderr)
            print("     ",e,file=sys.stderr)

        self.stopRebindButton.setDisabled(False)
        self.stopRebindButton.clicked.connect(self.unbindKeys)
        self.window().showMinimized()

    """
    
    This function is called when the "stop rebinding" key is pressed
    
    It unbind itself and unbind the remapping (rebinding)
    Enable back the elements that were disabled before and show back the window if it is minimized
    
    Event is set to None by default because it is not required when the stop button is clicked
    """
    def unbindKeys(self, event=None):
        try:
            keyboard.unremap_key(self.remap)
            keyboard.unhook_key(self.stopHotkeyEvent)
        except KeyError as e:
            print("Error while trying to unhook the keybinds:", file=sys.stderr)
            print("     ", e, file=sys.stderr)

        self.keyToRebindField.setDisabled(False)
        self.newKeyBindField.setDisabled(False)
        self.stopRebindingKey.setDisabled(False)
        self.rebindButton.setDisabled(False)

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