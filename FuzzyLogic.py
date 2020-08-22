import skfuzzy
import numpy as np
from skfuzzy import control as ctrl
from math import pi


class FuzzyLogic:
    velocityDif_in = ctrl.Antecedent(np.linspace(-500, 500, 1000), 'velocityDif')
    angleDif_in = ctrl.Antecedent(np.linspace(-pi/3, pi/3, 1000), 'angleDif')
    angularVelocity_in = ctrl.Antecedent(np.linspace(-2, 2, 1000), 'angularVelocity')

    forceY_out = ctrl.Consequent(np.linspace(0, 1500, 1000), 'forceY')
    rotationForce_out = ctrl.Consequent(np.linspace(-500, 500, 1000), 'rotationForce')

    velocityDif_in['smallPositive'] = skfuzzy.trimf(velocityDif_in.universe, [0, 0, 250])
    velocityDif_in['averagePositive'] = skfuzzy.trimf(velocityDif_in.universe, [0, 250, 500])
    velocityDif_in['bigPositive'] = skfuzzy.trimf(velocityDif_in.universe, [250, 500, 500])
    velocityDif_in['smallNegative'] = skfuzzy.trimf(velocityDif_in.universe, [-250, 0, 0])
    velocityDif_in['averageNegative'] = skfuzzy.trimf(velocityDif_in.universe, [-500, -250, 0])
    velocityDif_in['bigNegative'] = skfuzzy.trimf(velocityDif_in.universe, [-500, -500, -250])

    angleDif_in['small'] = skfuzzy.trimf(angleDif_in.universe, [-pi/12, 0, pi/12])
    angleDif_in['averagePositive'] = skfuzzy.trimf(angleDif_in.universe, [0, pi/12, pi/4])
    angleDif_in['bigPositive'] = skfuzzy.trimf(angleDif_in.universe, [pi/6, pi/3, pi/3])
    angleDif_in['averageNegative'] = skfuzzy.trimf(angleDif_in.universe, [-pi/4, -pi/12, 0])
    angleDif_in['bigNegative'] = skfuzzy.trimf(angleDif_in.universe, [-pi/3, -pi/3, -pi/6])

    angularVelocity_in['small'] = skfuzzy.trimf(angularVelocity_in.universe, [-1, 0, 1])
    angularVelocity_in['averagePositive'] = skfuzzy.trimf(angularVelocity_in.universe, [0, 1, 2])
    angularVelocity_in['bigPositive'] = skfuzzy.trimf(angularVelocity_in.universe, [1, 2, 2])
    angularVelocity_in['averageNegative'] = skfuzzy.trimf(angularVelocity_in.universe, [-2, -1, 0])
    angularVelocity_in['bigNegative'] = skfuzzy.trimf(angularVelocity_in.universe, [-2, -2, -1])

    rotationForce_out['small'] = skfuzzy.trimf(rotationForce_out.universe, [-50, 0, 50])
    rotationForce_out['averagePositive'] = skfuzzy.trimf(rotationForce_out.universe, [50, 100, 200])
    rotationForce_out['bigPositive'] = skfuzzy.trimf(rotationForce_out.universe, [150, 200, 200])
    rotationForce_out['hugePositive'] = skfuzzy.trimf(rotationForce_out.universe, [400, 500, 500])
    rotationForce_out['averageNegative'] = skfuzzy.trimf(rotationForce_out.universe, [-200, -100, -50])
    rotationForce_out['bigNegative'] = skfuzzy.trimf(rotationForce_out.universe, [-200, -200, -150])
    rotationForce_out['hugeNegative'] = skfuzzy.trimf(rotationForce_out.universe, [-500, -500, -400])

    forceY_out['small'] = skfuzzy.trimf(forceY_out.universe, [0, 0, 650])
    forceY_out['average'] = skfuzzy.trimf(forceY_out.universe, [600, 663.38, 740])
    forceY_out['big'] = skfuzzy.trimf(forceY_out.universe, [700, 1500, 1500])

    rule1 = ctrl.Rule(velocityDif_in['averageNegative'] | velocityDif_in['bigNegative'],
                      forceY_out['small'])
    rule2 = ctrl.Rule(velocityDif_in['smallPositive'] | velocityDif_in['smallNegative'],
                      forceY_out['average'])
    rule3 = ctrl.Rule(velocityDif_in['bigPositive'] | velocityDif_in['averagePositive'],
                      forceY_out['big'])

    rule4 = ctrl.Rule((angleDif_in['small'] & angularVelocity_in['small']),
                      rotationForce_out['small'])
    rule5 = ctrl.Rule((angleDif_in['small'] & angularVelocity_in['averageNegative']) |
                      (angleDif_in['averagePositive'] &
                      (angularVelocity_in['small'] | angularVelocity_in['averagePositive'])) |
                      (angleDif_in['averageNegative'] & angularVelocity_in['bigNegative']),
                      rotationForce_out['averagePositive'])
    rule6 = ctrl.Rule((angleDif_in['small'] & angularVelocity_in['bigNegative']) |
                      (angleDif_in['bigPositive'] & angularVelocity_in['bigPositive']) |
                      (angleDif_in['averagePositive'] & angularVelocity_in['averageNegative']),
                      rotationForce_out['bigPositive'])
    rule7 = ctrl.Rule((angleDif_in['averagePositive'] & angularVelocity_in['bigNegative']) |
                      (angleDif_in['bigPositive'] &
                      (angularVelocity_in['averageNegative'] | angularVelocity_in['bigNegative'] |
                       angularVelocity_in['small'] | angularVelocity_in['averagePositive'])),
                      rotationForce_out['hugePositive'])
    rule8 = ctrl.Rule((angleDif_in['small'] & angularVelocity_in['averagePositive']) |
                      (angleDif_in['averagePositive'] & angularVelocity_in['bigPositive']) |
                      (angleDif_in['averageNegative'] &
                      (angularVelocity_in['averageNegative'] | angularVelocity_in['small'])),
                      rotationForce_out['averageNegative'])
    rule9 = ctrl.Rule((angleDif_in['small'] & angularVelocity_in['bigPositive']) |
                      (angleDif_in['averageNegative'] & angularVelocity_in['averagePositive']) |
                      (angleDif_in['bigNegative'] & angularVelocity_in['bigNegative']),
                      rotationForce_out['bigNegative'])
    rule10 = ctrl.Rule((angleDif_in['averageNegative'] & angularVelocity_in['bigPositive']) |
                       (angleDif_in['bigNegative'] &
                        (angularVelocity_in['averagePositive'] | angularVelocity_in['bigPositive'] |
                        angularVelocity_in['small'] | angularVelocity_in['averageNegative'])),
                       rotationForce_out['hugeNegative'])

    control = ctrl.ControlSystem([rule1, rule2, rule3])
    controller = ctrl.ControlSystemSimulation(control)

    control1 = ctrl.ControlSystem([rule4, rule5, rule6, rule7, rule8, rule9, rule10])
    controller1 = ctrl.ControlSystemSimulation(control1)

    def GetForce(self, veloctiyDif):
        self.controller.input['velocityDif'] = veloctiyDif

        self.controller.compute()

        forceY = self.controller.output['forceY']

        return forceY

    def GetRotationForce(self, angleDif, angularVelocity):
        self.controller1.input['angleDif'] = angleDif
        self.controller1.input['angularVelocity'] = angularVelocity

        self.controller1.compute()

        rotationForce = self.controller1.output['rotationForce']

        return rotationForce
