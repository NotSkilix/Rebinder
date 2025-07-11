from PySide6 import QtCore, QtWidgets


from .type_def import KeyType


class Key(QtWidgets.QPushButton):
    def __init__(self, mainKey, secondaryKey=None, keyType : KeyType = KeyType.default):
        #TODO: manage keys size
        #TODO: Manage two keys (mainkey and secondary key)
        #TODO: Support images

        super().__init__()
        self.keyList = []

        if keyType == keyType.default:
            self.setText(mainKey)
            self.setStyleSheet("""
                            color: black
                            border-radius: 4px;
                            border: 1px solid #EDE7E7;
                            background: #FFF;
                            box-shadow: 0px 2px 0px 0px #EDE7E7;
                            """)
            self.setFixedSize(QtCore.QSize(44,34))