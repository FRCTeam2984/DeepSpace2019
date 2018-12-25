
import math

import ctre

from subsystems import drive
from constants import Constants
from pyfrc.physics import drivetrains, motion


class PhysicsEngine:

    X_WHEELBASE = 0.50
    Y_WHEELBASE = 0.62
    GRAVITY = 9.8

    def __init__(self, controller):
        self.controller = controller
        self.drive = drive.Drive()
        self.drivetrain = drivetrains.TwoMotorDrivetrain(
            deadzone=drivetrains.linear_deadzone(0.2))
        self.controller.add_device_gyro_channel('adxrs450_spi_0_angle')
        self.kl_encoder = Constants.DRIVE_ENCODER_TICKS_PER_REVOLUTION_LEFT / \
            Constants.WHEEL_CIRCUMFERENCE
        self.kr_encoder = Constants.DRIVE_ENCODER_TICKS_PER_REVOLUTION_RIGHT / \
            Constants.WHEEL_CIRCUMFERENCE

    def initialize(self, hal_data):
        pass

    def update_sim(self, hal_data, now, tm_diff):
        l_signal = hal_data['CAN'][Constants.LM_MOTOR_ID]['value']
        r_signal = hal_data['CAN'][Constants.RM_MOTOR_ID]['value']

        speed, rotation = self.drivetrain.get_vector(-l_signal, r_signal)

        hal_data['CAN'][Constants.LM_MOTOR_ID]['quad_position'] += int(
            self.drivetrain.l_speed * tm_diff * self.kl_encoder)
        hal_data['CAN'][Constants.RM_MOTOR_ID]['quad_position'] += int(
            self.drivetrain.r_speed * tm_diff * self.kr_encoder)

        self.controller.drive(speed, rotation, tm_diff)
