
import math

import ctre
from pyfrc.physics import drivetrains

import odemetry
from constants import Constants
from subsystems import drive
from utils import pose
import json
from pyfrc import config


class PhysicsEngine:

    def __init__(self, controller):
        self.controller = controller
        self.drive = drive.Drive()
        self.odemetry = odemetry.Odemetry()
        self.drivetrain = drivetrains.TwoMotorDrivetrain(
            x_wheelbase=Constants.WHEEL_BASE/12, speed=Constants.THEORETICAL_MAX_VELOCITY/12)
        self.starting_x = config.config_obj['pyfrc']['robot']['starting_x']*12
        self.starting_y = config.config_obj['pyfrc']['robot']['starting_y']*12

        # print("init {}".format(self.initial_x))
        self.kl_encoder = Constants.DRIVE_ENCODER_TICKS_PER_REVOLUTION_LEFT / \
            Constants.WHEEL_CIRCUMFERENCE  # / 12
        self.kr_encoder = Constants.DRIVE_ENCODER_TICKS_PER_REVOLUTION_RIGHT / \
            Constants.WHEEL_CIRCUMFERENCE  # / 12

    def initialize(self, hal_data):
        hal_data.setdefault('custom', {})

    def update_sim(self, hal_data, now, tm_diff):
        pos = self.controller.get_position()
        self.odemetry.pose = pose.Pose(
            pos[0]*12, pos[1]*12, pos[2])
        l_signal = hal_data['CAN'][Constants.LM_MOTOR_ID]['value']
        r_signal = hal_data['CAN'][Constants.RM_MOTOR_ID]['value']
        speed, rotation = self.drivetrain.get_vector(-l_signal, r_signal)

        hal_data['CAN'][Constants.LM_MOTOR_ID]['quad_position'] += int(
            self.drivetrain.l_speed * tm_diff * self.kl_encoder)
        hal_data['CAN'][Constants.RM_MOTOR_ID]['quad_position'] += int(
            self.drivetrain.r_speed * tm_diff * self.kr_encoder)

        self.controller.drive(speed, rotation, tm_diff)
        hal_data['custom']['Pose'] = [
            round(i, 2) for i in self.controller.get_position()]
