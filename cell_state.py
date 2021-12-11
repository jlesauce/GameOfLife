import enum


class CellState(enum.Enum):
    DEAD = 0
    ABOUT_TO_DIE = 1
    ALIVE = 2
    NONE = 3
