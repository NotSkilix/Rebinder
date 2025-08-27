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
    __isPlayButton = True

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
        self.__keyboard = KeyboardManager()

        # Field selectors
        self.__layoutComboBox = QtWidgets.QComboBox()
        self.__layoutComboBox.addItem("") # Populate the layout
        for layout in self.__keyboard.getAllLayouts():
            self.__layoutComboBox.addItem(layout)


        self.__sizeComboBox = QtWidgets.QComboBox()
        self.__sizeComboBox.hide()

        # Buttons
        self.__playAndStopButton = QtWidgets.QPushButton("Play")
        self.__playAndStopButton.setDisabled(True) # Disable it by default, will be re-enabled on first input

        # 'Build' the widget
        mainLayout = QtWidgets.QVBoxLayout(self)

        mainLayout.addWidget(title, alignment=QtCore.Qt.AlignmentFlag.AlignTop)
        mainLayout.addWidget(subtitle, alignment=QtCore.Qt.AlignmentFlag.AlignHCenter)
        mainLayout.addWidget(self.__layoutComboBox)
        mainLayout.addWidget(self.__sizeComboBox)
        mainLayout.addLayout(self.__keyboard)
        buttonLayout = QtWidgets.QHBoxLayout()
        buttonLayout.addWidget(self.__playAndStopButton)
        mainLayout.addLayout(buttonLayout)
        mainLayout.addSpacing(30)

        # Connect elements
        self.__playAndStopButton.clicked.connect(self.__onPlayOrStopTriggered) # Play/Stop button
        self.__keyboard.keyPressed.connect(self.__updateButtonStatus) # Keyboard - when a button is pressed
        self.__keyboard.stopKeyPressed.connect(self.__onPlayOrStopTriggered) # Keyboard - when the stop key is pressed
        self.__layoutComboBox.currentTextChanged.connect(self.__onLayoutFieldChanged) # Layout selector
        self.__sizeComboBox.currentTextChanged.connect(self.__switchKeyboard) # Size selector


    """
    __onPlayOrStopTriggered method is called when the play/stop button is clicked or when the stop key is pressed.
    
    It checks the state of the button and either starts or stops the rebinding process.
        - If the button is in play state, it runs the rebiding.
        - Else the button is in stop state so it stops the rebinding.
    """
    def __onPlayOrStopTriggered(self) -> None:
        if self.__isPlayButton:
            self.__updateRebindingState(True)
        else:
            self.__updateRebindingState(False)

    """
    updateButtonStatus method updates the status of the play/stop button based on whether the keys are playable.
    
    If the keys are playable, it enables the button; otherwise, it disables it.
    
    Args:
        isPlayable (bool): Indicates whether the keys are playable or not.
    """
    def __updateButtonStatus(self, isPlayable : bool) -> None:
        if isPlayable:
            self.__playAndStopButton.setDisabled(False)
        else:
            self.__playAndStopButton.setDisabled(True)


    """
    __updateRebindingState method updates the rebinding state of the keyboard by
    either playing or stopping the rebinding according to the argument.
    
    Args:
        state (bool): True to start rebinding, False to stop rebinding.
    """
    def __updateRebindingState(self, state : bool) -> None :
        # Play the rebinding
        if state:
            try:
                self.__keyboard.playRebinding()
            except Exception as e:
                self.createAndShowPopup(PopupTypes.ERROR, "Error on button click, the keybinds are invalid:", e)
                return

            self.__playAndStopButton.setText("Stop")
            self.window().showMinimized()

        # Stop the keyboard rebinding
        else:
            try:
                self.__keyboard.stopRebinding()
            except Exception as e:
                self.createAndShowPopup(PopupTypes.ERROR, "Error while trying to unhook the keybinds", e)
                return

            self.__playAndStopButton.setText("Play")

            # Show back the window if it was minimized
            if self.window().isMinimized():
                self.window().showNormal()

        # Change the button type
        self.__isPlayButton = not self.__isPlayButton

    """
    createAndShowPopup method creates and shows a popup dialog with the given type, title, and content.
    It is used to display error messages or other information to the user.
    
    Args:
        type (PopupTypes): The type of the popup (error, info, etc.).
        title (str): The title of the popup.
        content (Exception): The content to be displayed in the popup.
    """
    def createAndShowPopup(self, popupType : PopupTypes, title: str, content : Exception) -> None:
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

    """
    onLayoutFieldChanged method is called when the layout field is changed.
    """
    def __onLayoutFieldChanged(self) -> None:
        # Update the content of the sizeLayout field
        if self.__layoutComboBox.currentText() != "":
            self.__populateSizeSelector(self.__layoutComboBox.currentText())
        # Clear size layout when empty
        else:
            self.__sizeComboBox.hide()
            self.__keyboard.resetKeyboard()


    """
    populateSizeSelector method populates the size selector based on the selected layout.
    
    Args:
        layout (str): The selected keyboard layout.
    """
    def __populateSizeSelector(self, layout : str) -> None:
        self.__sizeComboBox.clear()
        self.__sizeComboBox.addItem("")
        sizes = self.__keyboard.getAvailableSizes(layout)
        for size in sizes:
            self.__sizeComboBox.addItem(size)

        # Show it when its hidden
        if self.__sizeComboBox.isHidden():
            self.__sizeComboBox.show()

    """
    switchKeyboard method switches the keyboard layout and size based on the current selections.
    
    Called when the size selection is changed (connected).
    """
    def __switchKeyboard(self) -> None:
        self.__keyboard.resetKeyboard()

        if self.__layoutComboBox.currentText() != "" and self.__sizeComboBox.currentText() != "":
            self.__keyboard.setKeyboard(self.__layoutComboBox.currentText(), self.__sizeComboBox.currentText())
