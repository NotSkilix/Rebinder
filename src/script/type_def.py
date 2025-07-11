from enum import Enum


class PopupTypes(Enum):
    Error = 1
    Info = 2

"""
Enumeration for the type of keys, the one with and without images.
"""
class KeyType(Enum):
    hasImage = 1,
    default = 2