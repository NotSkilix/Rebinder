from PySide6 import QtCore, QtWidgets


from .type_def import KeyType, KeyStyle


class Key(QtWidgets.QPushButton):
    def __init__(self, mainKey, secondaryKey=None, keyType : KeyType = KeyType.default):
        #TODO: manage keys size
        #TODO: Manage two keys (mainkey and secondary key)
        #TODO: Support images

        super().__init__()
        self.keyList = []

        if keyType == keyType.default:
            self.setText(mainKey)
            self.setStyleSheet(KeyStyle.default.value)
            self.setFixedSize(QtCore.QSize(44,34))


    """
    resetStatus method resets the key's style to the default style.
    """
    def resetStatus(self):
        self.setStyleSheet(KeyStyle.default.value)