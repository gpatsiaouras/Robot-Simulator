import numpy as np
import random

# from localization.main import Simulator
# from localization.robot import Robot


class Kalman:

    def __init__(self, robot):
        self.robot = robot
        # self.simulator = simulator

        self.n = 3
        self.predicted_state = np.zeros((self.n, 1))
        self.previous_state = np.zeros((self.n, 1))
        self.A = np.eye(3)
        self.B = np.matrix([[np.cos(self.robot.perceived_theta), 0],
                            [np.sin(self.robot.perceived_theta), 0],
                            [0, 1]
                            ])  # 1 because delta_t is 1.
        self.movement = np.matrix([[self.robot.linear_velocity], [self.robot.angular_velocity]])

        # initialize uncertainties with small values on diagonal of identity
        self.predicted_sigma_covariance = np.eye(self.n) * 0.001
        self.previous_sigma_covariance = np.eye(self.n) * 0.001

        # generate pseudo (for repeatability) random small numbers for initializing covariances
        np.random.seed(12)
        self.motion_model_covariance = np.eye(self.n) * np.random.uniform(0, 0.2)

        self.kalman = np.zeros(self.n)
        self.C = np.eye(self.n)

        self.sensor_model_covariance = np.eye(self.n) * np.random.uniform(0, 0.15)

        self.sensor_estimated_state = np.zeros(self.n)

        self.delta = np.eye(self.n) * np.random.uniform(0, 0.15)

        self.corrected_states_history = []
        self.predicted_states_history = []
        self.corrected_sigma_covariance_history = []

    def prediction(self, movement):
        self.movement = movement

        self.predicted_state = np.dot(self.A, self.previous_state) + np.dot(self.B, self.movement)
        self.predicted_sigma_covariance = self.A * self.previous_sigma_covariance * self.A.T + self.motion_model_covariance

        self.predicted_states_history.append(self.predicted_state)

    def correction(self, sensor_estimated_state):
        # self.sensor_estimated_state = sensor_estimated_state * self.C + self.delta
        self.sensor_estimated_state = sensor_estimated_state

        self.kalman = np.dot(np.dot(self.predicted_sigma_covariance, self.C.T), np.linalg.pinv(
            np.dot(np.dot(self.C, self.predicted_sigma_covariance),  self.C.T) + self.sensor_model_covariance))
        self.corrected_state = self.predicted_state + np.dot(self.kalman, (
                self.sensor_estimated_state - np.dot(self.C, self.predicted_state)))
        self.corrected_sigma = (np.eye(self.n) - self.kalman * self.C) * self.predicted_sigma_covariance

        self.corrected_states_history.append(self.corrected_state)
        self.corrected_sigma_covariance_history.append(self.corrected_sigma)

        self.previous_state = self.corrected_state
        self.predicted_sigma_covariance = self.corrected_sigma

        return self.corrected_state, self.corrected_sigma
