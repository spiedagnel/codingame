import sys
import math


# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

checkpoint_radius = 600

class Point(object):

    def __init__(self, x, y, vx=0, vy=0, angle=0, next_checkpoint=0, target=None, collision_threshold = 100):
        self.collision_threshold = collision_threshold
        self.dy = 0
        self.dx = 0
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.target = target
        self.angle = angle
        self.next_checkpoint = next_checkpoint
        self.set_next_next_checkpoint()
        self.hasBoost = True
        self.checkpoints_passed = 0

    def distance2(self, p):
        return (self.x - p.x) * (self.x - p.x) + (self.y - p.y) * (self.y - p.y)

    def distance(self, p):
        return math.sqrt(self.distance2(p))

    def set_next_next_checkpoint(self):
        global checkpoints
        self.next_next_checkpoint = 0 if self.next_checkpoint + 1 >= len(checkpoints) else self.next_checkpoint + 1

    def get_angle(self, p):
        d = self.distance(p)
        dx = (p.x - self.x) / d
        dy = (p.y - self.y) / d
        a_degrees = math.acos(dx) * 180.0 / math.pi
        if dy < 0:
            a_degrees = 360.0 - a_degrees
        return a_degrees

    def diff_angle(self, p):
        a = self.get_angle(p)
        right = a - self.angle if self.angle <= a else 360.0 - self.angle + a
        left = self.angle - a if self.angle >= a else self.angle + 360.0 - a

        if right < left:
            return right
        else:
            return -left

    def check_intersect(self, b):
        return intersect(self, Point(self.x+self.vx, self.y+self.vy), b, Point(b.x+b.vx, b.y+b.vy))

    def update_position(self, x, y, vx, vy, angle, next_checkpoint):
        self.vx = vx
        self.vy = vy
        self.dy = y - self.y
        self.dx = x - self.x
        self.x = x
        self.y = y
        self.angle = angle

        if next_checkpoint != self.next_checkpoint:
            self.next_checkpoint = next_checkpoint
            self.set_next_next_checkpoint()
            self.checkpoints_passed += 1

    def seek(self, t):
        # target = calculateGoal(self, target)
        target = Point(t.x, t.y)
        print("Target..." + str(target), file=sys.stderr)
        if lap > 0:
            if self.distance(target) > 1800:
                target.x -= 3.6 * self.dx
                target.y -= 3.6 * self.dy
            else:
                target.x -= 3.6 * self.dx
                target.y -= 3.6 * self.dy
        print("Target..." + str(target), file=sys.stderr)
        target_angle = self.diff_angle(target)
        # target_dist = self.distance(target)
        # Write an action using print
        # To debug: print("Debug messages...", file=sys.stderr)
        # rad = math.radians(target_angle)

        thrust = 100

        if lap > 0 and (target_angle > 90 or target_angle < -90):
            thrust = 0

        if check_collision(self, opponents):
            print("SHIELD...", file=sys.stderr)
            thrust_s = "SHIELD"
        elif self.hasBoost and t.x == max_checkpoint.x and t.y == max_checkpoint.y and 20 > target_angle > -20:
            self.hasBoost = False
            print("BOOST...", file=sys.stderr)
            thrust_s = "BOOST"
        else:
            thrust_s = str(thrust)
        return Move(target.x, target.y, thrust_s)

    def pursuit2(self, opponent1, opponent2):
        global checkpoints
        if self.target is None:
            self.target = opponent2
        if self.target == opponent1:
            other = opponent2
        else:
            other = opponent1
        if other.checkpoints_passed > self.target.checkpoints_passed:
            self.target = other
        checkpoint = checkpoints[self.target.next_checkpoint]
        checkpoint2 = checkpoints[self.target.next_next_checkpoint]
        target_checkpoint = Point(math.floor((self.target.x + checkpoint.x)/2), math.floor((self.target.y+checkpoint.y)/2))
        if self.distance(self.target) > 3.6 * target_checkpoint.distance(checkpoint):
            target_checkpoint = Point(math.floor((self.target.x + checkpoint2.x) / 2),
                                      math.floor((self.target.y + checkpoint2.y) / 2))
        move = self.seek(target_checkpoint)
        return move

    def next_move(self):
        global checkpoints
        global new_checkpoints
        points = checkpoints
        target = points[self.next_checkpoint]
        current_target_angle = self.diff_angle(target)
        current_target_dist = self.distance(target)

        if current_target_dist < 2000:
            target = new_checkpoints[self.next_checkpoint]
        elif current_target_dist < 1800 and 20 > current_target_angle > -20:
           # print(str(self.next_next_checkpoint) + " targeted...", file=sys.stderr)
            target = points[self.next_next_checkpoint]
        return self.seek(target)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __str__(self):
        return str(self.x) + " " + str(self.y) + "    " + str(self.vx) + " " + str(self.vy)


def ccw(A, B, C):
    return (C.y-A.y)*(B.x-A.x) > (B.y-A.y)*(C.x-A.x)


def intersect(A, B, C, D):
    return ccw(A, C, D) != ccw(B, C, D) and ccw(A, B, C) != ccw(A, B, D)


def check_collision(my_pod, other_pods):
    drag = 0.85
    threshold = 10
    my_future_position = Point(my_pod.x + my_pod.dx, my_pod.y + my_pod.dy)
    #print("My position..." + str(my_pod), file=sys.stderr)
    #print("My Future position..." + str(my_future_position), file=sys.stderr)
    for other in other_pods:
        #otherPredictedForce = other.velocity.multiplyScalar(1 / drag).subtract(other.lastVelocity);
        #otherPredictedVelocity = other.velocity.add(otherPredictedForce);
        other_predicted_position = Point(other.x+other.dx, other.y+other.dy)
        #print("other predicted..." + str(other_predicted_position), file=sys.stderr)
        #print("distance..." + str(other_predicted_position.distance(my_future_position)), file=sys.stderr)
        if abs(other_predicted_position.x - my_future_position.x) < 2 *radius \
            and abs(other_predicted_position.y - my_future_position.y) < 2 * radius\
                and (abs(my_pod.dx - other.dx) > my_pod.collision_threshold
                or abs(my_pod.dy - other.dy) > my_pod.collision_threshold):
                return True
    return False


class Move(object):
    def __init__(self, x, y, thrust):
        self.x = x
        self. y = y
        self.thrust = thrust

    def __str__(self):
        return str(math.floor(self.x)) + " " + str(math.floor(self.y)) + " " + self.thrust

number_laps = int(input())
radius = 400
number_checkpoints = int(input())
checkpoints = []
for j in range(number_checkpoints):
    x, y = input().split()
    checkpoints.append(Point(int(x), int(y)))

max_d = 0
max_checkpoint = None
for j in range(len(checkpoints)-1):
    d = checkpoints[j].distance2(checkpoints[j + 1])
    if d > max_d:
        max_d = d
        max_checkpoint = checkpoints[j + 1]
d = checkpoints[len(checkpoints)-1].distance2(checkpoints[0])
if d > max_d:
    max_d = d
    max_checkpoint = checkpoints[0]

new_checkpoints = []
for j in range(number_checkpoints):
    a = checkpoints[j]
    b = checkpoints[0 if j + 1 >= len(checkpoints) else j + 1]
    dist = a.distance(b)
    new_checkpoints.append(Point(math.floor(a.x + (checkpoint_radius - 100) * (b.x - a.x)/dist), math.floor(a.y + (checkpoint_radius - 100) * (b.y - a.y)/dist)))

boost = False
my_pod1 = Point(0, 0, 0, 0, 0, 0, collision_threshold=300)
my_pod2 = Point(0, 0, 0, 0, 0, 0, collision_threshold=50)
opponent1 = Point(0, 0, 0, 0, 0, 0)
opponent2 = Point(0, 0, 0, 0, 0, 0)
opponents = [opponent1, opponent2]
lap = 0
runner = my_pod1
blocker = my_pod2
# game loop
while True:
    # next_checkpoint_x: x position of the next check point
    # next_checkpoint_y: y position of the next check point
    # next_checkpoint_dist: distance to the next checkpoint
    # next_checkpoint_angle: angle between your pod orientation and the direction of the next checkpoint
    x, y, dx, dy, angle, next_checkpoint = [int(i) for i in input().split()]
    my_pod1.update_position(x, y, dx, dy, angle, next_checkpoint)
    x, y, dx, dy, angle, next_checkpoint = [int(i) for i in input().split()]
    my_pod2.update_position(x, y, dx, dy, angle, next_checkpoint)
    x, y, dx, dy, angle, next_checkpoint = [int(i) for i in input().split()]
    opponent1.update_position(x, y, dx, dy, angle, next_checkpoint)
    x, y, dx, dy, angle, next_checkpoint = [int(i) for i in input().split()]
    opponent2.update_position(x, y, dx, dy, angle, next_checkpoint)
    
    # You have to output the target position
    # followed by the power (0 <= thrust <= 100)
    # i.e.: "x y thrust"
    if blocker.checkpoints_passed > runner.checkpoints_passed:
        runner, blocker = blocker, runner
    print(runner.next_move())
    #print(my_pod2.next_move())
    print(blocker.pursuit2(opponent1, opponent2))
    lap += 1
