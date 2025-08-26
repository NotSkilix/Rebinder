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
            QPushButton {
                color: black;
                font-size: 16px;
                font-weight: bold;
                border-radius: 6px;
                border: 1px solid #999;
                background: white;
                box-shadow: 0px 2px 2px rgba(0, 0, 0, 0.2);
                padding: 4px 0px;
                margin: 2px;
                border-bottom: 6px solid #999;
            }
            
            QPushButton:pressed {
                border-bottom: 2px solid #999;
            }
            
            QPushButton:hover {
                background: #b3b3b3;
            }
              """
    KEY_TO_CHANGE = """
                QPushButton {
                    color: black;
                    font-size: 16px;
                    font-weight: bold;
                    border-radius: 6px;
                    border: 1px solid #999;
                    background: #A15EC0;
                    padding: 4px 0px;
                    margin: 2px;
                    background-color: #A15EC0;
                    border-bottom: 6px solid #763993;
                }
                
                QPushButton:pressed {
                    border-bottom: 2px solid #763993;
                }
                
                QPushButton:hover {
                    background: #8540a5;
                }
                  """
    NEW_KEY = """
                QPushButton {
                    color: black;
                    font-size: 16px;
                    font-weight: bold;
                    border-radius: 6px;
                    border: 1px solid #999;
                    background: #6AC05E;
                    padding: 4px 0px;
                    margin: 2px;
                    background-color: #6AC05E;
                    border-bottom: 6px solid #449339;
                }
                
                QPushButton:pressed {
                    border-bottom: 2px solid #449339;
                }
                
                QPushButton:hover {
                    background: #4ca540;
                }
             """
    STOP_KEY = """
                QPushButton {
                    color: black;
                    font-size: 16px;
                    font-weight: bold;
                    border-radius: 6px;
                    border: 1px solid #999;
                    background: #D5681A;
                    padding: 4px 0px;
                    margin: 2px;
                    background-color: #D5681A;
                    border-bottom: 4px solid #b65916;
                }
                
                QPushButton:pressed {
                    border-bottom: 2px solid #b65916;
                }
                
                QPushButton:hover {
                    background: #b65916;
                }
              """

class KeySize(Enum):
    BASIC = QtCore.QSize(55, 55)  # Esc, F1, A, etc.
    TAB = QtCore.QSize(87, 41)  # Tab
    CAPS_LOCK_BACKSPACE = QtCore.QSize(74, 41)  # Caps Lock, Backspace
    LEFT_SHIFT_ENTER_NUMPAD_0 = QtCore.QSize(109, 41)  # Left Shift, Enter, Numpad 0
    RIGHT_SHIFT = QtCore.QSize(127, 41)  # Right Shift
    SPACE = QtCore.QSize(272, 41)  # Space
    NUMPAD_PLUS_ENTER = QtCore.QSize(55, 81)  # Numpad +, Numpad Enter