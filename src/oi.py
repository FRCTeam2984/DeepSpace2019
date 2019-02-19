from utils import joystick, singleton, intakestate, hatchlatchstate, gamestate
from constants import Constants
from wpilib.buttons.joystickbutton import JoystickButton
from commands import sethatchlatchstate, drivetimed, setintakestate, setlongarm, setgamestate, rollclimbroller


class OI(metaclass=singleton.Singleton):
    """Deals with anything controller related,
    be it gamepads, joysticks, or steering wheels."""

    def __init__(self):
        self.driver = joystick.Joystick(
            Constants.DRIVER_PORT, Constants.DRIVER_X_MOD, Constants.DRIVER_Y_MOD, Constants.DRIVER_Z_MOD, Constants.DRIVER_T_MOD)
        self.operator = joystick.Joystick(
            Constants.OPERATOR_PORT, Constants.OPERATOR_X_MOD, Constants.OPERATOR_Y_MOD, Constants.OPERATOR_Z_MOD, Constants.OPERATOR_T_MOD)

        self.drive_buttons = [
            self.driver.getJoystickButton(n) for n in range(1, 13)]
        self.operator_buttons = [
            self.operator.getJoystickButton(n) for n in range(1, 13)]

        self.intake_suck = setintakestate.SetIntakeState(
            intakestate.IntakeState.SUCK)
        self.intake_spit = setintakestate.SetIntakeState(
            intakestate.IntakeState.SPIT)
        self.intake_stop = setintakestate.SetIntakeState(
            intakestate.IntakeState.STOP)
        self.hatch_close = sethatchlatchstate.SetHatchLatchState(
            hatchlatchstate.HatchLatchState.CLOSE)
        self.hatch_open = sethatchlatchstate.SetHatchLatchState(
            hatchlatchstate.HatchLatchState.OPEN)
        self.hatch_toggle = sethatchlatchstate.SetHatchLatchState(
            hatchlatchstate.HatchLatchState.TOGGLE)
        self.game_stow = setgamestate.SetGameState(gamestate.GameState.STOW)
        self.game_play = setgamestate.SetGameState(gamestate.GameState.PLAY)
        self.game_start_climb = setgamestate.SetGameState(
            gamestate.GameState.START_CLIMB)
        self.game_end_climb = setgamestate.SetGameState(
            gamestate.GameState.END_CLIMB)
        self.game_end_game = setgamestate.SetGameState(
            gamestate.GameState.END_GAME)
        self.climb_roll = rollclimbroller.RollClimbRoller(
            Constants.CLIMB_ROLLER_SPEED)
        self.climb_stop = rollclimbroller.RollClimbRoller(0)

        self.scoot_left = drivetimed.DriveTimed(
            0, -Constants.SCOOT_SPEED, 0, Constants.SCOOT_DURATION)
        self.scoot_right = drivetimed.DriveTimed(
            0, Constants.SCOOT_SPEED, 0, Constants.SCOOT_DURATION)

        self.operator_buttons[0].whenPressed(self.game_stow)
        self.operator_buttons[1].whenPressed(self.game_play)
        self.operator_buttons[2].whenPressed(self.game_start_climb)
        self.operator_buttons[3].whenPressed(self.game_end_climb)
        # self.operator_buttons[4].whenPressed(self.intake_spit)
        # self.operator_buttons[4].whenReleased(self.intake_stop)
        # self.operator_buttons[5].whenPressed(self.intake_suck)
        # self.operator_buttons[5].whenReleased(self.intake_stop)

        self.drive_buttons[4].whenPressed(self.scoot_left)
        self.drive_buttons[5].whenPressed(self.scoot_right)

        self.operator_buttons[4].whenPressed(self.climb_roll)
        self.operator_buttons[4].whenReleased(self.climb_stop)

        self.operator_buttons[6].whenPressed(self.hatch_close)
        self.operator_buttons[7].whenPressed(self.hatch_open)
