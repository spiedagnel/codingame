import sys
import math


# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

class Point(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def distance2(self, p):
        return (self.x - p.x) * (self.x - p.x) + (self.y - p.y) * (self.y - p.y)

    def distance(self, p):
        return math.sqrt(self.distance2(p))

    def get_angle(self, p):
        d = self.distance(p)
        dx = (p.x - self.x) / d
        dy = (p.y - self.y) / d
        a_degrees = math.acos(dx) * 180.0 / math.pi
        if (dy < 0):
            a_degrees = 360.0 - a_degrees
        return a_degrees

    def update_position(self, x, y):
        self.dx = x - self.x
        self.dy = y - self.y
        self.d2 = self.dx * self.dx + self.dy * self.dy
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.__dict__ == other.__dict__


class Move(object):
    def __init(self, angle, thrust):
        self.angle = angle
        self.thrust = thrust


hasBoost = True
previous_next_checkpoint_dist = 0
checkpoints = list()
max_d_checkpoint = Point(0, 0)
prev_next_checkpoint = Point(0, 0)
max_checkpoint_dist = 0
checkpoint_counter = 0
boost = False
first_turn = True
my_pod = Point(0, 0)
# game loop
while True:
    # next_checkpoint_x: x position of the next check point
    # next_checkpoint_y: y position of the next check point
    # next_checkpoint_dist: distance to the next checkpoint
    # next_checkpoint_angle: angle between your pod orientation and the direction of the next checkpoint
    x, y, next_checkpoint_x, next_checkpoint_y, next_checkpoint_dist, next_checkpoint_angle = [int(i) for i in
                                                                                               input().split()]
    opponent_x, opponent_y = [int(i) for i in input().split()]
    my_pod.update_position(x, y)
    next_checkpoint = Point(next_checkpoint_x, next_checkpoint_y)
    if next_checkpoint != prev_next_checkpoint:
        checkpoint_counter += 1
        if not (first_turn) and checkpoint_counter >= len(checkpoints):
            checkpoint_counter = 0
        prev_next_checkpoint = next_checkpoint
        if first_turn:
            if next_checkpoint in checkpoints:
                checkpoint_counter = 1
                first_turn = False
            else:
                checkpoints.append(next_checkpoint)
                if next_checkpoint_dist > max_checkpoint_dist:
                    max_checkpoint_dist = next_checkpoint_dist
                    max_d_checkpoint = next_checkpoint
        else:
            if next_checkpoint == max_d_checkpoint:
                boost = True
                print("Boost...", file=sys.stderr)
                # print(str(checkpoint_counter)+ " ...", file=sys.stderr)

    if not first_turn and next_checkpoint_dist < 1200 and 20 > target_angle > -20:
        print(str(checkpoint_counter) + " targeted..." + str(next_checkpoint_dist) + " " + str(my_pod.d2),
              file=sys.stderr)
        next_next_checkpoint = checkpoints[checkpoint_counter]
        target = next_next_checkpoint
        target_angle = my_pod.get_angle(next_next_checkpoint)
        target_dist = my_pod.distance(next_next_checkpoint)
    else:
        target = next_checkpoint
        target_angle = next_checkpoint_angle
        target_dist = next_checkpoint_dist

    adjx = 0
    adjy = 0
    if target.x - my_pod.x > 0 > my_pod.dx:
        adjx = 150
    elif target.x - my_pod.x < 0 < my_pod.dx:
        adjx = -150

    if target.y - my_pod.y > 0 > my_pod.dy:
        adjy = 150
    elif target.y - my_pod.y < 0 < my_pod.dy:
        adjy = -150

    # Write an action using print
    # To debug: print("Debug messages...", file=sys.stderr)
    rad = math.radians(target_angle)

    thrust = 100
    if target_angle > 90 or target_angle < -90:
        thrust = 0
    else:
        perfectForce = target_dist * math.cos(rad) * 0.13;
        if perfectForce > 100:
            thrust = 100
        elif perfectForce < 0:
            thrust = 0
        else:
            thrust = int(perfectForce)

            # if next_checkpoint_dist < 1000 and next_checkpoint_dist < previous_next_checkpoint_dist:
            #   thrust = 50

    if boost and hasBoost and next_checkpoint_dist > 4000 and next_checkpoint_angle == 0:
        hasBoost = False
        thrustS = "BOOST"
    else:
        thrustS = str(thrust)
    # You have to output the target position
    # followed by the power (0 <= thrust <= 100)
    # i.e.: "x y thrust"
    print(str(target.x + adjx ) + " " + str(target.y + adjy) + " " + thrustS)
