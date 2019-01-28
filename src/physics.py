
import math

import ctre
from pyfrc.physics import drivetrains

import odemetry
from constants import Constants
from subsystems import drive
from utils import pose, units
import json
from pyfrc import config


class PhysicsEngine:

    def __init__(self, controller):
        self.controller = controller
        self.drive = drive.Drive()
        self.odemetry = odemetry.Odemetry()
        self.drivetrain = drivetrains.MecanumDrivetrain(x_wheelbase=units.inchesToFeet(Constants.X_WHEEL_BASE), y_wheelbase=units.inchesToFeet(
            Constants.Y_WHEEL_BASE), speed=units.inchesToFeet(Constants.THEORETICAL_MAX_VELOCITY))
        self.starting_x = units.feetToInches(
            config.config_obj['pyfrc']['robot']['starting_x'])
        self.starting_y = units.feetToInches(
            config.config_obj['pyfrc']['robot']['starting_y'])

        # self.kl_encoder = Constants.DRIVE_ENCODER_TICKS_PER_REVOLUTION_LEFT / \
        #     Constants.WHEEL_CIRCUMFERENCE
        # self.kr_encoder = Constants.DRIVE_ENCODER_TICKS_PER_REVOLUTION_RIGHT / \
        #     Constants.WHEEL_CIRCUMFERENCE

    def initialize(self, hal_data):
        hal_data.setdefault('custom', {})

    def update_sim(self, hal_data, now, tm_diff):
        pos = self.controller.get_position()
        self.odemetry.pose = pose.Pose(
            units.feetToInches(pos[0]), units.feetToInches(pos[1]), pos[2])
        fl_signal = hal_data['CAN'][Constants.FL_MOTOR_ID]['value']
        fr_signal = hal_data['CAN'][Constants.FR_MOTOR_ID]['value']
        bl_signal = hal_data['CAN'][Constants.BL_MOTOR_ID]['value']
        br_signal = hal_data['CAN'][Constants.BR_MOTOR_ID]['value']

        x_speed, y_speed, rotation = self.drivetrain.get_vector(
            bl_signal, br_signal, fl_signal, fr_signal)
        # hal_data['CAN'][Constants.LM_MOTOR_ID]['quad_position'] += int(
        #     self.drivetrain.l_speed * tm_diff * self.kl_encoder)
        # hal_data['CAN'][Constants.RM_MOTOR_ID]['quad_position'] += int(
        #     self.drivetrain.r_speed * tm_diff * self.kr_encoder)

        self.controller.vector_drive(x_speed, y_speed, rotation, tm_diff)
        hal_data['custom']['Pose'] = [
            round(i, 2) for i in self.controller.get_position()]
