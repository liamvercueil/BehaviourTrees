import py_trees
import random

class Robot():
    '''
    Sample robot class with possible methods to test a behaviour tree.
    These methods do NOT yet provide any functionality, so use with caution...
    '''
    def __init__(self):
        pass
    
    def isBallVisible(self) -> bool:
        decision = random.choice([True, False])
        return decision
    
    def searchForBall(self):
        # some code to search for the ball...
        action_result = random.choice(["Success", "Fail"])
        return action_result
        
    def getDistanceFromBall(self, distance = 1) -> float:
        return distance
            
    def goToBall(self):
        action_result = random.choice(["Success", "Fail"])
        return action_result
    
    def startDribbler(self):
        action_result = random.choice(["Success", "Fail"])
        return action_result
    
    def canShoot(self) -> bool:
        decision = random.choice([True, False])
        return decision

    def shoot(self):
        action_result = random.choice(["Success", "Fail"])
        return action_result


# THE FOLLOWING CLASSES ARE TO BE USED IN BEHAVIOUR TREE (BT) IMPLEMENTATION

'''
NOTES:

You'll notice that in the following lines I have represented various nodes as classes.

Why use classes instead of methods?
    1. PyTrees requires nodes to be class-like
    2. More flexible and reusable than traditional functions
    3. Methods are unable to maintain state (like RUNNING, SUCCESS, FAILURE)
    4. Separate each decision/action logic; cleaner design

Each node features a constructor method and an update method.
update() will return the current state of the node: later, logging and feedback messages will be added...

Robot is a requirement each time you want to instantiate a node. Passing a shared robot across all nodes 
is more efficient, saves state, and preserves resources. An alternative is to use blackboard via PyTrees.
'''

class IsBallVisible(py_trees.behaviour.Behaviour):
    def __init__(self, robot: Robot):
        super().__init__(name="IsBallVisible")
        self.robot = robot

    def update(self):
        ready_to_start = random.choice([True, False])
        if ready_to_start is False:
            return py_trees.common.Status.RUNNING
        else:
            if self.robot.isBallVisible():
                return py_trees.common.Status.SUCCESS
            else: 
                return py_trees.common.Status.FAILURE

class SearchForBall(py_trees.behaviour.Behaviour):
    def __init__(self, robot: Robot):
        super().__init__(name="SearchForBall")
        self.robot = robot

    def update(self):
        ready_to_start = random.choice([True, False])
        if ready_to_start is False:
            return py_trees.common.Status.RUNNING
        else:
            if self.robot.searchForBall() == "Success":
                return py_trees.common.Status.SUCCESS
            else: 
                return py_trees.common.Status.FAILURE

class IsClose(py_trees.behaviour.Behaviour):
    # Include threshold as an argument for the function so we can specify how close the threshold distance is
    def __init__(self, robot: Robot, threshold: int):
        super().__init__(name="IsClose")
        self.robot = robot
        self.threshold = threshold

    def update(self):
        ready_to_start = random.choice([True, False])
        if ready_to_start is False:
            return py_trees.common.Status.RUNNING
        else:    
            if self.robot.getDistanceFromBall() > self.threshold:
                return py_trees.common.Status.SUCCESS
            else:
                return py_trees.common.Status.FAILURE

class GoToBall(py_trees.behaviour.Behaviour):
    def __init__(self, robot: Robot):
        super().__init__(name="GoToBall")
        self.robot = robot

    def update(self):
        ready_to_start = random.choice([True, False])
        if ready_to_start is False:
            return py_trees.common.Status.RUNNING
        else:
            if self.robot.goToBall() == "Success":
                return py_trees.common.Status.SUCCESS
            else: 
                return py_trees.common.Status.FAILURE

class StartDribbler(py_trees.behaviour.Behaviour):
    def __init__(self, robot: Robot):
        super().__init__(name="StartDribber")
        self.robot = robot

    def update(self):
        ready_to_start = random.choice([True, False])
        if ready_to_start is False:
            return py_trees.common.Status.RUNNING
        else:
            if self.robot.startDribbler() == "Success":
                return py_trees.common.Status.SUCCESS
            else: 
                return py_trees.common.Status.FAILURE

class CanShoot(py_trees.behaviour.Behaviour):
    def __init__(self, robot: Robot):
        super().__init__(name="CanShoot")
        self.robot = robot

    def update(self):
        ready_to_start = random.choice([True, False])
        if ready_to_start is False:
            py_trees.common.Status.RUNNING
        else:
            if self.robot.canShoot():
                return py_trees.common.Status.SUCCESS
            else:
                return py_trees.common.Status.FAILURE

class Shoot(py_trees.behaviour.Behaviour):
    def __init__(self, robot: Robot):
        super().__init__(name="Shoot")
        self.robot = robot

    def update(self):
        ready_to_start = random.choice([True, False])
        if ready_to_start is False:
            return py_trees.common.Status.RUNNING
        else:
            if self.robot.shoot() == "Success":
                return py_trees.common.Status.SUCCESS
            else: 
                return py_trees.common.Status.FAILURE

def build_tree(agent):
    # === Root Sequence ===
    root = py_trees.composites.Sequence("Root Sequence")

    # --- 1. Selector ---
    selector_1 = py_trees.composites.Selector("Ball Visible?")
    is_ball_visible = IsBallVisible(agent)
    search_for_ball = SearchForBall(agent)
    selector_1.add_children([is_ball_visible, search_for_ball])

    # --- 2. Sequence ---
    sequence_2 = py_trees.composites.Sequence("Approach Ball")

    # 2.1 Selector
    selector_2_1 = py_trees.composites.Selector("Close Enough?")
    is_close = IsClose(agent)
    go_to_ball = GoToBall(agent)
    selector_2_1.add_children([is_close, go_to_ball])

    # 2.2 StartDribbler
    start_dribbler = StartDribbler(agent)

    sequence_2.add_children([selector_2_1, start_dribbler])

    # --- 3. Sequence ---
    sequence_3 = py_trees.composites.Sequence("Shoot Ball")
    can_shoot = CanShoot(agent)
    shoot = Shoot(agent)
    sequence_3.add_children([can_shoot, shoot])

    # === Add everything to root ===
    root.add_children([selector_1, sequence_2, sequence_3])

    print(py_trees.display.unicode_tree(root, show_status=True))
    return root

# ==== Main ====

def main():
    agent = Robot()
    behaviour_tree = build_tree(agent)
    behaviour_tree.setup_with_descendants()

    while True:
        behaviour_tree.tick()
