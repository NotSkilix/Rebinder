from PySide6 import QtCore, QtWidgets


from .type_def import KeyType, KeyStyle, KeySize


class Key(QtWidgets.QPushButton):
    def __init__(self, mainKey, secondaryKey=None, keyType : KeyType = KeyType.default, keySize : KeySize = KeySize.BASIC):
        #TODO: Support images
        super().__init__()

        if keyType == keyType.default:
            self.setText(mainKey)
            self.setStyleSheet(KeyStyle.default.value)
            self.setMinimumSize(keySize.value)
            self.setMinimumSize(keySize.value)


    """
    resetStatus method resets the key's style to the default style.
    """
    def resetStatus(self):
        self.setStyleSheet(KeyStyle.default.value)