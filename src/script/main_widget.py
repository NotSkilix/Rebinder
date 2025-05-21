import keyboard
import sys

from PySide6 import QtCore, QtWidgets, QtGui
from .type_def import PopupTypes

"""
MainWidget class is the main widget of the rebinder application.
It provides a GUI for rebinding keys and stopping the rebinding process.

Attributes:
    isPlayButton (bool): Indicates whether the play button is currently active.
    remap (keyboard.remap_key): The remapped key.
    stopHotkeyEvent (keyboard.hook_key): The event to stop the rebinding.
"""
class MainWidget(QtWidgets.QWidget):
    isPlayButton = True
    listOfFields = []

    """
    Constructor for MainWidget.
    
    Initializes the GUI elements and layout for the rebinder application.
    """
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
        self.listOfFields.append(self.keyToRebindField)

        keyToRebinLayout = QtWidgets.QHBoxLayout()
        keyToRebinLayout.addWidget(keyToRebindText)
        keyToRebinLayout.addWidget(self.keyToRebindField)

        # NewKeyBind layout & elements
        newKeyBindText = QtWidgets.QLabel("Write the new keybind (b, F4,...): ")
        self.newKeyBindField = QtWidgets.QLineEdit(maxLength=6, placeholderText="New bind...")
        self.listOfFields.append(self.newKeyBindField)

        newKeyBindLayout = QtWidgets.QHBoxLayout()
        newKeyBindLayout.addWidget(newKeyBindText)
        newKeyBindLayout.addWidget(self.newKeyBindField)

        # StopRebinding layout & elements
        stopRebindingText = QtWidgets.QLabel("The keybind to stop the rebinding: ")
        self.stopRebindingKeyField = QtWidgets.QLineEdit(maxLength=6, placeholderText="Stop rebinding key...")
        self.listOfFields.append(self.stopRebindingKeyField)

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
        self.playAndStopButton.clicked.connect(self.onplayAndStopButtonClick) # Button click
        self.keyToRebindField.textEdited.connect(self.checkFields) # Text edit
        self.newKeyBindField.textEdited.connect(self.checkFields) # Text edit
        self.stopRebindingKeyField.textEdited.connect(self.checkFields) # Text edit


    """
    onplayAndStopButtonClick method is called when the play/stop button is clicked.
    
    It checks the state of the button and either starts or stops the rebinding process.
        - If the button is in play state, it calls the playRebinding method.
        - If the button is in stop state, it calls the stopRebinding method.
    """
    def onplayAndStopButtonClick(self):
        if self.isPlayButton:
            self.playRebinding()
        else:
            self.stopRebinding()

    """
    Called by "onplayAndStopButtonClick" when the play button is clicked.
    
    It checks the input fields for validity and starts the rebinding process.
    Disable the input fields and changes the button text to "Stop".
    """
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
        except ValueError as e:
            self.createAndShowPopup(PopupTypes.Error,
                                    "Error on button click, one or more fields must be empty or have a the same keybind:",e)
            return

        # Rebind the keys
        try:
            self.remap = keyboard.remap_key(self.keyToRebindField.text(), self.newKeyBindField.text())
        except Exception as e:
            self.createAndShowPopup(PopupTypes.Error, "Error on button click, the keybinds are invalid:", e)
            return

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
    Called by "onplayAndStopButtonClick" when the stop button is clicked.
    
    It unbinds the keys and re-enables the input fields.
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
    createAndShowPopup method creates and shows a popup dialog with the given type, title, and content.
    It is used to display error messages or other information to the user.
    
    Args:
        type (PopupTypes): The type of the popup (error, info, etc.).
        title (str): The title of the popup.
        content (Exception): The content to be displayed in the popup.
    """
    def createAndShowPopup(self, type : PopupTypes, title: str, content : Exception):
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

    """
    checkFields method checks the content of the input fields and highlights similar fields.
    It removes any existing highlights and re-applies them if needed.
    """
    def checkFields(self):
        self.removeHover() # Remove all the hovers and re-applicate them if needed

        # Check the fields content
        i = 0
        for field in self.listOfFields:
            for nextField in self.listOfFields[1+i:]:
                if field.text() != "" and field.text() == nextField.text():
                    print("if")
                    self.addHover([field, nextField])
            i+=1


    """
    addHover method adds a hover effect to the specified fields and disables the play button.
    """
    def addHover(self, similarLabels : list):
        # Background color
        for similarLabel in similarLabels:
            similarLabel.setStyleSheet("background-color: red")

        # Disable the play button
        self.playAndStopButton.setDisabled(True)


    """
    removeHover method removes the hover effect from all fields and re-enables the play button.
    """
    def removeHover(self):
        # Remove hover and background in the fields
        for elements in self.listOfFields:
            elements.setStyleSheet("background-color: none")

        # Re-enable the play button
        self.playAndStopButton.setDisabled(False)