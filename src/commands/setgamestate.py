from wpilib.command import CommandGroup

from subsystems import intake
from utils.gamestate import GameState
from commands import setshortarm, setlongarm
from constants import Constants


class SetGameState(CommandGroup):
    def __init__(self, state):
        super().__init__()
        self.state = state

    def initialize(self):
        posture = Constants.GAME_STATES[self.state]
        self.addParallel(setshortarm.SetShortArm(posture[0]))
        self.addParallel(setlongarm.SetLongArm(posture[2]))

    def end(self):
        pass
