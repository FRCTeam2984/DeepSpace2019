from constants import Constants


def inchesToFeet(inches):
    """Convert inches to feet."""
    return inches/12


def feetToInches(inches):
    """Convert inches to feet."""
    return inches*12


def metersToInches(meters):
    """Convert meters to inches."""
    return meters * 39.3701


def inchesToMeters(inches):
    """Convert inches to meters."""
    return inches * 0.0254


def metersPer100msToInchesPerSec(meters_per_100ms):
    """Convert meters per 100ms to inches per sec (ctre uses meters/100ms)."""
    return metersToInches(meters_per_100ms * 10)


def inchesPerSecToMetersPer100ms(inches_per_sec):
    """Convert inches/sec to meters/100ms (ctre uses meters/100ms)."""
    return inchesToMeters(inches_per_sec/10)


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
