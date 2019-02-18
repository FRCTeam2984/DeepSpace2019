from enum import Enum


class GameState(Enum):
    STOW = 0
    PLAY = 1
    START_CLIMB = 2
    END_CLIMB = 3
    END_GAME = 4
