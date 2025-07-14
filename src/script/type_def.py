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
    keyToChange = """
                    background-color: purple
                  """
    newKey = """
               background-color: green
             """
    stopKey = """
                background-color: orange
              """