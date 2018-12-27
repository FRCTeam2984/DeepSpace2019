
import math

import ctre

from subsystems import drive
from constants import Constants
from pyfrc.physics import drivetrains, motion

import odemetry



class PhysicsEngine:

    def __init__(self, controller):
        self.controller = controller
        self.drive = drive.Drive()
        self.odemetry = odemetry.Odemetry()
        self.drivetrain = drivetrains.TwoMotorDrivetrain(
            x_wheelbase=Constants.WHEEL_BASE, speed=Constants.THEORETICAL_MAX_SPEED)
        self.initial_x = self.controller.get_position()[0]
        self.initial_y = self.controller.get_position()[1]

        self.kl_encoder = Constants.DRIVE_ENCODER_TICKS_PER_REVOLUTION_LEFT / \
            Constants.WHEEL_CIRCUMFERENCE / 12
        self.kr_encoder = Constants.DRIVE_ENCODER_TICKS_PER_REVOLUTION_RIGHT / \
            Constants.WHEEL_CIRCUMFERENCE / 12

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

        hal_data['custom']['Pose'] = [round(i,3) for i in self.controller.get_position()]
