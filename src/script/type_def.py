from enum import Enum


class PopupTypes(Enum):
    Error = 1
    Info = 2

"""
Enumeration for the type of keys, the one with and without images.
"""
class KeyType(Enum):
    hasImage = 1
    default = 2

"""
Enumeration for the status of a key in the keyboard.
"""
class KeyStatus(Enum):
    keyToChange = 1
    newKey = 2
    stopKey = 3

"""
Enumeration for the style of keys in the keyboard.
"""
class KeyStyle(Enum):
    default = """
                color: black;
                font-size: 16px;
                font-weight: bold;
                border-radius: 6px;
                border: 1px solid #999;
                background: white;
                box-shadow: 0px 2px 2px rgba(0, 0, 0, 0.2);
                padding: 4px 0px;
                min-width: 44px;
                min-height: 34px;
                max-width: 44px;
                max-height: 34px;
                margin: 2px;
              """
    keyToChange = """
                    color: black;
                    font-size: 16px;
                    font-weight: bold;
                    border-radius: 6px;
                    border: 1px solid #999;
                    background: #A15EC0;
                    box-shadow: 0px 2px 2px #A15EC0;
                    padding: 4px 0px;
                    min-width: 44px;
                    min-height: 34px;
                    max-width: 44px;
                    max-height: 34px;
                    margin: 2px;
                    background-color: #A15EC0
                  """
    newKey = """
                color: black;
                font-size: 16px;
                font-weight: bold;
                border-radius: 6px;
                border: 1px solid #999;
                background: #6AC05E;
                box-shadow: 0px 2px 2px #6AC05E;
                padding: 4px 0px;
                min-width: 44px;
                min-height: 34px;
                max-width: 44px;
                max-height: 34px;
                margin: 2px;
                background-color: #6AC05E
             """
    stopKey = """
                color: black;
                font-size: 16px;
                font-weight: bold;
                border-radius: 6px;
                border: 1px solid #999;
                background: #D5681A;
                box-shadow: 0px 2px 2px #D5681A;
                padding: 4px 0px;
                min-width: 44px;
                min-height: 34px;
                max-width: 44px;
                max-height: 34px;
                margin: 2px;
                background-color: #D5681A
              """