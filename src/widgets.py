import keyboard
import sys

from PySide6 import QtCore, QtWidgets, QtGui

class MainWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        # Widget settings
        self.setWindowTitle("Rebinder V0.1")

        # Generic widget text
        title = QtWidgets.QLabel("Rebinder", alignment=QtCore.Qt.AlignmentFlag.AlignHCenter)
        title.setFont(QtGui.QFont("Arial", 24))
        bottom = QtWidgets.QLabel("Made with ❤ by NotSkilix", alignment=QtCore.Qt.AlignmentFlag.AlignHCenter)
        bottom.setFont(QtGui.QFont("Arial", 11))

        # keyToRebind layout & text
        keyToRebindText = QtWidgets.QLabel("Write a key to rebind (a, F3,...):")
        self.keyToRebindField = QtWidgets.QLineEdit(maxLength=5, placeholderText="Key to rebind...") #TODO: Look if 5 char is enough for all keybinds

        keyToRebinLayout = QtWidgets.QHBoxLayout()
        keyToRebinLayout.addWidget(keyToRebindText)
        keyToRebinLayout.addWidget(self.keyToRebindField)

        # NewKeyBind layout & text
        NewKeyBindText = QtWidgets.QLabel("Write the new keybind (b, F4,...):")
        self.newKeyBindField = QtWidgets.QLineEdit(maxLength=5, placeholderText="New bind...") #TODO: Look if 5 char is enough for all keybinds

        NewKeyBindLayout = QtWidgets.QHBoxLayout()
        NewKeyBindLayout.addWidget(NewKeyBindText)
        NewKeyBindLayout.addWidget(self.newKeyBindField)

        # Rebind Button
        self.rebindButton = QtWidgets.QPushButton("Rebind")

        # 'Build' the widget
        mainLayout = QtWidgets.QVBoxLayout(self)
        mainLayout.addWidget(title)
        mainLayout.addLayout(keyToRebinLayout)
        mainLayout.addLayout(NewKeyBindLayout)
        mainLayout.addWidget(self.rebindButton)
        mainLayout.addWidget(bottom)

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
        except ValueError as e:
            print("Error on button click, one or more fields must be empty: ",  file=sys.stderr)
            print("     ",e,file=sys.stderr)
            return
        try:
            keyboard.remap_key(self.keyToRebindField.text(), self.newKeyBindField.text())
        except ValueError as e:
            print("Error on button click, one of the keybind but be incorrect/inexistant: ",  file=sys.stderr)
            print("     ",e,file=sys.stderr)
            return