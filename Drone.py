from pymunk import *
from math import pi, cos
import tensorflow as tf
import numpy as np
from FuzzyLogic import FuzzyLogic


class Drone:
    weight = 1.368
    leftFanForce = [0, 0]
    rightFanForce = [0, 0]
    moveDirection = [False, False, False, False]
    turned = False
    body = Body()
    shapes = []
    neuralNetwork = tf.keras.models.load_model("./my_model")
    fuzzyLogic = FuzzyLogic()
    logicModel = "Neural Network"

    def __init__(self):
        self.body.position = 650, 40
        self.shapes.append(Poly(self.body, [(0, 20), (24, 20), (12, 0)]))
        self.shapes.append(Poly(self.body, [(80, 20), (104, 20), (92, 0)]))
        self.shapes.append(Poly(self.body, [(40, 7), (40, 20), (64, 20), (64, 7)]))
        self.shapes.append(Segment(self.body, (22, 13), (40, 13), 2))
        self.shapes.append(Segment(self.body, (64, 13), (83, 13), 2))
        self.data = np.zeros((1, 9))
        weights = [self.weight / 5, self.weight / 5, 2 * self.weight / 5, self.weight / 10, self.weight / 10]
        for i in range(len(weights)):
            self.shapes[i].mass = weights[i]
            self.shapes[i].color = (217, 217, 217, 255)

    def GetDrone(self):
        return self.body, self.shapes

    def GetForces(self):
        if self.moveDirection[0]:
            self.turned = True
        self.data[0][0] = self.turned
        self.data[0][1] = self.moveDirection[0]
        self.data[0][2] = self.moveDirection[1]
        self.data[0][3] = self.moveDirection[2]
        self.data[0][4] = self.moveDirection[3]
        self.data[0][5] = self.body.angle
        self.data[0][6] = self.body.velocity[0]
        self.data[0][7] = self.body.velocity[1]
        self.data[0][8] = self.body.angular_velocity
        predict = self.neuralNetwork.predict(self.data, batch_size=1)
        self.leftFanForce[1] = predict[0][0]
        self.rightFanForce[1] = predict[0][1]

    def MoveVertically(self):
        forceY = 0
        if self.moveDirection[0]:
            forceY = self.fuzzyLogic.GetForce(250 - self.body.velocity[1] * cos(self.body.angle))
            self.turned = True
        elif self.moveDirection[1]:
            forceY = self.fuzzyLogic.GetForce(-250 - self.body.velocity[1] * cos(self.body.angle))
        elif self.turned:
            forceY = self.fuzzyLogic.GetForce(-self.body.velocity[1] * cos(self.body.angle))
        self.leftFanForce[1] = forceY / cos(self.body.angle)
        self.rightFanForce[1] = forceY / cos(self.body.angle)

    def Rotate(self):
        if self.turned and self.moveDirection[2]:
            rotationForce = self.fuzzyLogic.GetRotationForce(-pi / 6 - self.body.angle, self.body.angular_velocity)
            self.leftFanForce[1] -= rotationForce
        elif self.turned and self.moveDirection[3]:
            rotationForce = self.fuzzyLogic.GetRotationForce(pi / 6 - self.body.angle, self.body.angular_velocity)
            self.rightFanForce[1] += rotationForce
        else:
            rotationForce = self.fuzzyLogic.GetRotationForce(-self.body.angle * 2, self.body.angular_velocity)
            if self.body.angle > 0:
                self.leftFanForce[1] -= rotationForce
            else:
                self.rightFanForce[1] += rotationForce

    def Move(self):
        if self.logicModel == "Neural Network":
            self.GetForces()
        else:
            self.MoveVertically()
            self.Rotate()
        self.body.apply_force_at_local_point(self.leftFanForce, (12, 40 / 3))
        self.body.apply_force_at_local_point(self.rightFanForce, (92.1, 40 / 3))
        if self.body.position[1] <= 40 and not self.moveDirection[0]:
            self.turned = False

    def GetStringInfo(self):
        string1 = "Force: "
        string1 += str(int(self.leftFanForce[1])) + ", " + str(int(self.rightFanForce[1]))
        string2 = "Rotation: "
        string2 += str(int(self.body.angle / pi * 180 * 10) / 10)
        string3 = "Velocity: "
        string3 += str(int(int(self.body.velocity[0] * 100) / 100 * cos(abs(self.body.angle)))) + ", " + str(int(
                int(self.body.velocity[1] * 100) / 100 * cos(abs(self.body.angle))))
        string4 = "Angular velocity: "
        string4 += str(int(self.body.angular_velocity * 100) / 100)
        string5 = "Position: "
        string5 += str(int(self.body.position[0])) + ", " + str(int(self.body.position[1]))
        return string1, string2, string3, string4, string5, self.logicModel
