from typing import override
from PySide6 import QtWidgets

from src.types.type_def import KeyType, KeyStyle, KeySize

"""
Key class represents a key in the keyboard.

It inherits from QPushButton and is used to create a button that represents a key on the keyboard.

Attributes:
    __keySize (KeySize): The size of the key.
    __keyStyle (KeyStyle): The style of the key.
"""
class Key(QtWidgets.QPushButton):
    __keySize : KeySize = KeySize.BASIC
    __keyStyle : KeyStyle = KeyStyle.DEFAULT

    def __init__(self, mainKey, secondaryKey=None, keyType: KeyType = KeyType.DEFAULT,
                 keySize: KeySize = KeySize.BASIC):
        #TODO: Support images
        super().__init__()

        self.__keySize = keySize

        if keyType == keyType.DEFAULT:
            self.setText(mainKey)
            self.setStyleSheet(KeyStyle.DEFAULT)
            self.__setSize()

    """
    resetStatus method resets the key's style to the default style.
    """
    def resetStatus(self):
        self.setStyleSheet(KeyStyle.DEFAULT)

    def __setSize(self):
        self.setMinimumSize(self.__keySize.value)
        self.setMaximumSize(self.__keySize.value)

    """
    setStyleSheet method sets the style sheet for the key and ensures that the 
    minimum size is set correctly.
    
    Args:
        style (str): The style sheet to be applied to the key.
        
    """
    @override
    def setStyleSheet(self, style : KeyStyle):
        self.__keyStyle = style

        super().setStyleSheet(self.__keyStyle.value)

        self.__setSize()