import numpy as np
import random

from localization.main import Simulator
from localization.robot import Robot


class Kalman:

    def __init__(self, robot: Robot, simulator: Simulator):

        self.robot = robot
        self.simulator = simulator

        self.n = 3
        self.predicted_state = np.zeros(self.n)
        self.previous_state = np.zeros(self.n)
        self.A = np.eye(3)
        self.B = np.matrix([[np.cos(self.robot.noiseless_theta), 0],
                            [np.sin(self.robot.noiseless_theta), 0],
                            0, 1]) # 1 because delta_t is 1.
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

    def prediction(self, ):
        self.predicted_state = self.A * self.previous_state + self.B * self.movement
        self.predicted_sigma_covariance = self.A * self.previous_sigma_covariance * self.A.T + self.motion_model_covariance

    def correction(self):
        self.kalman = self.predicted_sigma_covariance * self.C.T * np.linalg.inv(self.C * self.predicted_sigma_covariance * self.C.T + self.sensor_model_covariance)
        self.corrected_state = self.predicted_state + self.kalman * (self.sensor_estimated_state - self.C * self.predicted_state)
        self.corrected_sigma = (np.eye(self.n) - self.kalman * self.C) * self.predicted_sigma_covariance

        return self.corrected_state, self.corrected_sigma






#
#     # first and second state coordinates third one identifies the landmark
#     landmarks = np.zeros((6, 3))
#
#     # uniformly distribute field of movement and arrange..?
#
#     print(landmarks)
#
#     sensor_radius = 10
#
#     # constantly check if landmarks distance from robot is less than sensor radius..
#     # if correct apply kalman filter...
#
#     robot_position = np.array([0, 0, 0])  # np.zeros(3) or np.zeros ((3)) or np.zeros((0,3)) or np.zeros((1,3))
#     robot_covariance = np.zeros((3, 3))
#
#     for i in np.arange(0, 3, 1):
#         robot_covariance[i, i] = (random.random() / 10)  # specify later
#     print(robot_covariance)
#
#     # motion model..
#     # allow modeling of motion errors?
#
#     # update position..
#     # (mu = Au + Bu)
#
#     # difference mu and u??
#
#     mean = robot_position#
#     # first and second state coordinates third one identifies the landmark
#     landmarks = np.zeros((6, 3))
#
#     # uniformly distribute field of movement and arrange..?
#
#     print(landmarks)
#
#     sensor_radius = 10
#
#     # constantly check if landmarks distance from robot is less than sensor radius..
#     # if correct apply kalman filter...
#
#     robot_position = np.array([0, 0, 0])  # np.zeros(3) or np.zeros ((3)) or np.zeros((0,3)) or np.zeros((1,3))
#     robot_covariance = np.zeros((3, 3))
#
#     for i in np.arange(0, 3, 1):
#         robot_covariance[i, i] = (random.random() / 10)  # specify later
#     print(robot_covariance)
#
#     # motion model..
#     # allow modeling of motion errors?
#
#     # update position..
#     # (mu = Au + Bu)
#
#     # difference mu and u??
#
#     mean = robot_position
#     covariance = robot_covariance  # I think this is the starting covariance value.
#
#     # the robot should know where it starts..
#
#     time_step = 1  # .. is this time step different from the other one..?
#
#     # PREDICITION
#     # create prediction function
#
#     # ambiguopus name..
#     movement = np.array([0, 0])  # here go the velocities..  (how do we calculate??)
#
#     # I THINK THIS ARE THE CorrecT THING TO EXTRACT
#     # v (vl + vr) /2
#     # w v/R (from above..), sounds reasonable..
#
#     A = np.array([
#         [1, 0, 0],
#         [0, 1, 0],
#         [0, 0, 1]])
#
#     B = np.array([
#         [time_step * np.cos(robot_position[2]), 0],
#         [time_step * np.sin(robot_position[2]), 0],
#         [0, time_step]])
#
#     R = np.zeros((3, 3))  # covariance matrix defines noise motion model
#
#     for i in np.arange(0, 3, 1):  # could use length Q to make more compact
#         R[i, i] = (0.1)  # specify later
#     print(R)
#
#     mean_pred = np.dot(A, mean) + np.dot(B, movement)  # update mean..
#
#     # A_inverse = numpy.linalg.inv(A) #not actually necessary..?
#
#     covariance_pred = np.dot(A, np.dot(covariance, A.T)) + R  # As A is identity, R basically adds some noise
#
#     # plot or store ?
#
#     ##I am getting a feeling some sort of trade-off between time to calculate position (..more off the later?),
#     ##but each time location claculated adds uncertainty..
#
#     # CORRECTION
#     # watch out for mean and covariances names..
#
#     C = np.identity(3)  # this is the variable I understand worse..
#
#     Q = np.zeros((3, 3))  # covariance matrix defines noise of sensor model
#     for i in np.arange(0, 3, 1):
#         Q[i, i] = (0.1)  # specify later
#     print(Q)
#
#     K_part = np.linalg.inv(np.dot(C, np.dot(covariance_pred, C.T)) + Q)
#     K = np.dot(covariance_pred, np.dot(C.T, K_part))
#
#     # z =  # below calculations
#
#     I = np.identity(3)
#
#     mean = mean_pred + np.dot(K, (z - np.dot(C, mean_pred)))
#     covariance = np.dot((I - np.dot(K, C)), covariance_pred)
#
#     # z calculations
#     # could be all inside a function that estimates location from sensors (includes signal receiving)
#
#     # show communication robot landmark..
#
#
# def signal(self, landmarks, robot_position):  # makes sense for it to be the correct one
#     r = np.sqrt(
#         np.power((landmarks[i][0] - robot_position[0]), 2) + np.power((landmarks[i][1] - robot_position[1]), 2))
#     theta = np.arctan2((landmarks[i][1] - robot_position[1]), (landmarks[i][0] - robot_position[0])) - \
#             robot_position[2]
#     s = landmarks[i][2]
#     return r, theta, s
#
#
# measurements = np.zeros((6, 4))  # not sure if best way.. could just append somehow
#
# # receive and collect neighbouring signals
# measurement_count = 0
# for i in np.arange(0, 6, 1):
#     # checking = landmarks[i] #just the landmark we are using
#     # check if any landmark is within receiving distance..
#     distance = np.sqrt(
#         np.power((landmarks[i][0] - robot_position[0]), 2) + np.power((landmarks[i][1] - robot_position[1]),
#                                                                       2))  # same as used in signal..
#     if distance < radius:
#         measurement_count += 1
#         measurements[i][0], measurements[i][1], measurements[i][2] = signal(
#             landmarks[i])  # the robot receives the signal
#         # not sure about assignment above
#         measurements[i][3] = 1  # there is a measurement in this box..
#
#
# # slighlty different robot functioning, but I think it respects the model..
#
# def estimate_location(self):
#     pass
#
#
# # uses map knowledge and signal information
#
# # determine mapping from neighbouring sigmas..
# estimations = np.zeros((6, 4))
# for i in np.arange(0, 6, 1):
#     z = estimate_location()
#     if measurement[i][4] = 1:
#         # call landmark placement
#         landmark
#         z
#
# # Finally obtain value of z, then process that..
#
# # Experiment to see at what point the robot gets completely lost, no matter what, or changing some things..

#     covariance = robot_covariance  # I think this is the starting covariance value.
#
#     # the robot should know where it starts..
#
#     time_step = 1  # .. is this time step different from the other one..?
#
#     # PREDICITION
#     # create prediction function
#
#     # ambiguopus name..
#     movement = np.array([0, 0])  # here go the velocities..  (how do we calculate??)
#
#     # I THINK THIS ARE THE CorrecT THING TO EXTRACT
#     # v (vl + vr) /2
#     # w v/R (from above..), sounds reasonable..
#
#     A = np.array([
#         [1, 0, 0],
#         [0, 1, 0],
#         [0, 0, 1]])
#
#     B = np.array([
#         [time_step * np.cos(robot_position[2]), 0],
#         [time_step * np.sin(robot_position[2]), 0],
#         [0, time_step]])
#
#     R = np.zeros((3, 3))  # covariance matrix defines noise motion model
#
#     for i in np.arange(0, 3, 1):  # could use length Q to make more compact
#         R[i, i] = (0.1)  # specify later
#     print(R)
#
#     mean_pred = np.dot(A, mean) + np.dot(B, movement)  # update mean..
#
#     # A_inverse = numpy.linalg.inv(A) #not actually necessary..?
#
#     covariance_pred = np.dot(A, np.dot(covariance, A.T)) + R  # As A is identity, R basically adds some noise
#
#     # plot or store ?
#
#     ##I am getting a feeling some sort of trade-off between time to calculate position (..more off the later?),
#     ##but each time location claculated adds uncertainty..
#
#     # CORRECTION
#     # watch out for mean and covariances names..
#
#     C = np.identity(3)  # this is the variable I understand worse..
#
#     Q = np.zeros((3, 3))  # covariance matrix defines noise of sensor model
#     for i in np.arange(0, 3, 1):
#         Q[i, i] = (0.1)  # specify later
#     print(Q)
#
#     K_part = np.linalg.inv(np.dot(C, np.dot(covariance_pred, C.T)) + Q)
#     K = np.dot(covariance_pred, np.dot(C.T, K_part))
#
#     # z =  # below calculations
#
#     I = np.identity(3)
#
#     mean = mean_pred + np.dot(K, (z - np.dot(C, mean_pred)))
#     covariance = np.dot((I - np.dot(K, C)), covariance_pred)
#
#     # z calculations
#     # could be all inside a function that estimates location from sensors (includes signal receiving)
#
#     # show communication robot landmark..
#
#
# def signal(self, landmarks, robot_position):  # makes sense for it to be the correct one
#     r = np.sqrt(
#         np.power((landmarks[i][0] - robot_position[0]), 2) + np.power((landmarks[i][1] - robot_position[1]), 2))
#     theta = np.arctan2((landmarks[i][1] - robot_position[1]), (landmarks[i][0] - robot_position[0])) - \
#             robot_position[2]
#     s = landmarks[i][2]
#     return r, theta, s
#
#
# measurements = np.zeros((6, 4))  # not sure if best way.. could just append somehow
#
# # receive and collect neighbouring signals
# measurement_count = 0
# for i in np.arange(0, 6, 1):
#     # checking = landmarks[i] #just the landmark we are using
#     # check if any landmark is within receiving distance..
#     distance = np.sqrt(
#         np.power((landmarks[i][0] - robot_position[0]), 2) + np.power((landmarks[i][1] - robot_position[1]),
#                                                                       2))  # same as used in signal..
#     if distance < radius:
#         measurement_count += 1
#         measurements[i][0], measurements[i][1], measurements[i][2] = signal(
#             landmarks[i])  # the robot receives the signal
#         # not sure about assignment above
#         measurements[i][3] = 1  # there is a measurement in this box..
#
#
# # slighlty different robot functioning, but I think it respects the model..
#
# def estimate_location(self):
#     pass
#
#
# # uses map knowledge and signal information
#
# # determine mapping from neighbouring sigmas..
# estimations = np.zeros((6, 4))
# for i in np.arange(0, 6, 1):
#     z = estimate_location()
#     if measurement[i][4] = 1:
#         # call landmark placement
#         landmark
#         z
#
# # Finally obtain value of z, then process that..
#
# # Experiment to see at what point the robot gets completely lost, no matter what, or changing some things..
