from constants import Constants
import math


def radiansToDegrees(radians):
    """Convert radians to degrees."""
    return math.degrees(radians)


def degreesToRadians(degrees):
    """Convert degrees to radians."""
    return math.radians(degrees)


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


def inchesToTicksLeft(inches):
    """Convert inches to ticks for the left encoder."""
    return (inches*Constants.CPR_DRIVE_BL)/Constants.WHEEL_CIRCUMFERENCE


def inchesToTicksRight(inches):
    """Convert inches to ticks for the right encoder."""
    return (inches*Constants.CPR_DRIVE_BR)/Constants.WHEEL_CIRCUMFERENCE


def ticksToInchesLeft(ticks):
    """Convert ticks to inches for the left encoder."""
    return (ticks/Constants.CPR_DRIVE_BL)*Constants.WHEEL_CIRCUMFERENCE


def ticksToInchesRight(ticks):
    """Convert ticks to inches for the right encoder."""
    return (ticks/Constants.CPR_DRIVE_BR)*Constants.WHEEL_CIRCUMFERENCE


def inchesPerSecToTicksPer100msLeft(inches_per_sec):
    """Convert ticks per 100ms to inches per sec for the left encoder (ctre uses ticks/100ms)."""
    return inchesToTicksLeft(inches_per_sec)/10


def inchesPerSecToTicksPer100msRight(inches_per_sec):
    """Convert ticks per 100ms to inches per sec for the right encoder (ctre uses ticks/100ms)."""
    return inchesToTicksRight(inches_per_sec)/10


def ticksPer100msToInchesPerSecLeft(ticks_per_100ms):
    """Convert inches per sec to ticks per 100ms for the left encoder (ctre uses ticks/100ms)."""
    return ticksToInchesLeft(ticks_per_100ms)*10


def ticksPer100msToInchesPerSecRight(ticks_per_100ms):
    """Convert inches per sec to ticks per 100ms for the right encoder (ctre uses ticks/100ms)."""
    return ticksToInchesRight(ticks_per_100ms)*10
