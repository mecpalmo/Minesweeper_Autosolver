from enum import Enum

class Field(Enum):
    
    UNDETERMINED = 99
    OPEN_EMPTY = 0
    OPEN_MINE = 98
    CLOSED_UNKNOWN = 97
    CLOSED_FLAG = 96