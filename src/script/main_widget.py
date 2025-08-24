from PySide6 import QtCore, QtWidgets, QtGui

from src.types.type_def import PopupTypes
from src.script.keyboard_manager import KeyboardManager

"""
MainWidget class is the main widget of the rebinder application.
It provides a GUI for rebinding keys and stopping the rebinding process.

Attributes:
    isPlayButton (bool): Indicates whether the play button is currently active.
"""
class MainWidget(QtWidgets.QWidget):
    isPlayButton = True

    """
    Constructor for MainWidget.
    
    Initializes the GUI elements and layout for the rebinder application.
    """
    def __init__(self):
        super().__init__()

        # Window settings
        self.setWindowTitle("Rebinder V0.4")
        self.setStyleSheet("background-color: #1E1E1E;")

        # Generic widget text
        title = QtWidgets.QLabel("Press your keys", alignment=QtCore.Qt.AlignmentFlag.AlignHCenter)
        title.setFont(QtGui.QFont("Arial", 24))
        subtitle = QtWidgets.QLabel("You can press multiple time the same key to change its purpose", alignment=QtCore.Qt.AlignmentFlag.AlignHCenter)
        subtitle.setFont(QtGui.QFont("Arial", 11))

        # Keyboard Grid
        self.keyboard = KeyboardManager()

        # Buttons
        self.playAndStopButton = QtWidgets.QPushButton("Play")
        self.playAndStopButton.setDisabled(True) # Disable it by default, will be re-enabled on first input

        # 'Build' the widget
        mainLayout = QtWidgets.QVBoxLayout(self)

        mainLayout.addWidget(title, alignment=QtCore.Qt.AlignmentFlag.AlignTop)
        mainLayout.addWidget(subtitle, alignment=QtCore.Qt.AlignmentFlag.AlignHCenter)
        mainLayout.addLayout(self.keyboard)
        buttonLayout = QtWidgets.QHBoxLayout()
        buttonLayout.addWidget(self.playAndStopButton)
        mainLayout.addLayout(buttonLayout)
        mainLayout.addSpacing(30)

        # Connect elements
        self.playAndStopButton.clicked.connect(self.onplayAndStopButtonClick) # Play/Stop button
        self.keyboard.keyPressed.connect(self.updateButtonStatus) # Keyboard - when a button is pressed
        self.keyboard.stopKeyPressed.connect(self.stopRebinding) # Keyboard - when the stop key is pressed


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
    updateButtonStatus method updates the status of the play/stop button based on whether the keys are playable.
    
    If the keys are playable, it enables the button; otherwise, it disables it.
    
    Args:
        isPlayable (bool): Indicates whether the keys are playable or not.
    """
    def updateButtonStatus(self, isPlayable):
        if isPlayable:
            self.playAndStopButton.setDisabled(False)
        else:
            self.playAndStopButton.setDisabled(True)


    """
    playRebinding method starts the rebinding process by calling the keyboard's playRebinding method.
    
    It also changes the play/stop button text to "Stop" and minimizes the window.
    """
    def playRebinding(self):
        try:
            self.keyboard.playRebinding()
        except Exception as e:
            self.createAndShowPopup(PopupTypes.ERROR, "Error on button click, the keybinds are invalid:", e)
            return

        self.playAndStopButton.setText("Stop")
        self.window().showMinimized()

        # Change the button type
        self.isPlayButton = not self.isPlayButton


    """
    stopRebinding method stops the rebinding process and resets the keyboard state.
    
    It also changes the play/stop button text and restores the window if it was minimized.
    If an error occurs while stopping the rebinding, it shows an error popup.
    """
    def stopRebinding(self):
        # Stop the keyboard rebinding
        try:
            self.keyboard.stopRebinding()
        except Exception as e:
            self.createAndShowPopup(PopupTypes.ERROR, "Error while trying to unhook the keybinds", e)
            return

        self.playAndStopButton.setText("Play")

        # Show back the window if it was minimized
        if self.window().isMinimized():
            self.window().showNormal()

        # Change the button type
        self.isPlayButton = not self.isPlayButton


    """
    createAndShowPopup method creates and shows a popup dialog with the given type, title, and content.
    It is used to display error messages or other information to the user.
    
    Args:
        type (PopupTypes): The type of the popup (error, info, etc.).
        title (str): The title of the popup.
        content (Exception): The content to be displayed in the popup.
    """
    def createAndShowPopup(self, popupType : PopupTypes, title: str, content : Exception):
        popup = QtWidgets.QDialog(self)

        if popupType == PopupTypes.ERROR:
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