"""
This module contains type definitions and enumerations used in the keyboard application.
"""

from PySide6 import QtCore
from enum import Enum

"""
Path to the JSON file containing keyboard layouts.
"""
KEYBOARD_LAYOUT_PATH = "src/data/keyboard_layouts.json"

class PopupTypes(Enum):
    ERROR = 1
    INFO = 2

"""
Enumeration for the type of keys, the one with and without images.
"""
class KeyType(Enum):
    HAS_IMAGE = 1
    DEFAULT = 2

"""
Enumeration for the status of a key in the keyboard.
"""
class KeyStatus(Enum):
    KEY_TO_CHANGE = 1
    NEW_KEY = 2
    STOP_KEY = 3

"""
Enumeration for the style of keys in the keyboard.
"""
class KeyStyle(Enum):
    DEFAULT = """
                color: black;
                font-size: 16px;
                font-weight: bold;
                border-radius: 6px;
                border: 1px solid #999;
                background: white;
                box-shadow: 0px 2px 2px rgba(0, 0, 0, 0.2);
                padding: 4px 0px;
                margin: 2px;
              """
    KEY_TO_CHANGE = """
                    color: black;
                    font-size: 16px;
                    font-weight: bold;
                    border-radius: 6px;
                    border: 1px solid #999;
                    background: #A15EC0;
                    box-shadow: 0px 2px 2px #A15EC0;
                    padding: 4px 0px;
                    margin: 2px;
                    background-color: #A15EC0
                  """
    NEW_KEY = """
                color: black;
                font-size: 16px;
                font-weight: bold;
                border-radius: 6px;
                border: 1px solid #999;
                background: #6AC05E;
                box-shadow: 0px 2px 2px #6AC05E;
                padding: 4px 0px;
                margin: 2px;
                background-color: #6AC05E
             """
    STOP_KEY = """
                color: black;
                font-size: 16px;
                font-weight: bold;
                border-radius: 6px;
                border: 1px solid #999;
                background: #D5681A;
                box-shadow: 0px 2px 2px #D5681A;
                padding: 4px 0px;
                margin: 2px;
                background-color: #D5681A
              """

class KeySize(Enum):
    BASIC = QtCore.QSize(55, 55)  # Esc, F1, A, etc.
    TAB = QtCore.QSize(87, 41)  # Tab
    CAPS_LOCK_BACKSPACE = QtCore.QSize(74, 41)  # Caps Lock, Backspace
    LEFT_SHIFT_ENTER_NUMPAD_0 = QtCore.QSize(109, 41)  # Left Shift, Enter, Numpad 0
    RIGHT_SHIFT = QtCore.QSize(127, 41)  # Right Shift
    SPACE = QtCore.QSize(272, 41)  # Space
    NUMPAD_PLUS_ENTER = QtCore.QSize(55, 81)  # Numpad +, Numpad Enter