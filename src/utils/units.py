from constants import Constants


def inchesToFeet(inches):
    """Convert inches to feet."""
    return inches/12


def feetToInches(inches):
    """Convert inches to feet."""
    return inches*12


def inchesToTickLeft(inches):
    """Convert inches to ticks for the left encoder."""
    return (inches*Constants.DRIVE_ENCODER_TICKS_PER_REVOLUTION_LEFT)/Constants.WHEEL_CIRCUMFERENCE


def inchesToTickRight(inches):
    """Convert inches to ticks for the right encoder."""
    return (inches*Constants.DRIVE_ENCODER_TICKS_PER_REVOLUTION_RIGHT)/Constants.WHEEL_CIRCUMFERENCE


def ticksToInchesLeft(ticks):
    """Convert ticks to inches for the left encoder."""
    return (ticks/Constants.DRIVE_ENCODER_TICKS_PER_REVOLUTION_LEFT)*Constants.WHEEL_CIRCUMFERENCE


def ticksToInchesRight(ticks):
    """Convert ticks to inches for the right encoder."""
    return (ticks/Constants.DRIVE_ENCODER_TICKS_PER_REVOLUTION_RIGHT)*Constants.WHEEL_CIRCUMFERENCE
