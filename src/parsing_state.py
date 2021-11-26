from enum import Enum


class ParsingState(Enum):
    NORMAL_STATE = 1
    BACK_STATE = 2
    FINAL_STATE = 3
    ERROR_STATE = 4