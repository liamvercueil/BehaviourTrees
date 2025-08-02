import py_trees

class Robot():
    '''
    Sample robot class with possible methods to complete the behaviour tree.
    These methods do NOT yet provide any functionality, so use with caution...
    '''
    def __init__(self):
        pass
    
    def isBallVisible(self):
        pass
    
    def searchForBall(self):
        pass

    def getDistanceFromBall(self):
        pass
    
    def goToBall(self):
        pass
    
    def startDribbler(self):
        pass
    
    def canShoot(self):
        pass

    def shoot(self):
        pass


# THE FOLLOWING CLASSES ARE TO BE USED IN BEHAVIOUR TREE (BT) IMPLEMENTATION

'''
NOTES:

You'll notice that in the following lines we have represented various nodes as classes.

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
        if self.robot.isBallVisible():
            return py_trees.common.Status.SUCCESS
        else: 
            return py_trees.common.Status.FAILURE

class SearchForBall(py_trees.behaviour.Behaviour):
    def __init__(self, robot: Robot):
        super().__init__(name="SearchForBall")
        self.robot = robot

    def update(self):
        try:
            self.robot.searchForBall()
            return py_trees.common.Status.SUCCESS
        except:
            return py_trees.common.Status.FAILURE

class IsClose(py_trees.behaviour.Behaviour):
    # Include threshold as an argument for the function so we can specify how close the threshold distance is
    def __init__(self, robot: Robot, threshold: int):
        super().__init__(name="IsClose")
        self.robot = robot
        self.threshold = threshold

    def update(self):
        if self.robot.getDistanceFromBall() > self.threshold:
            return py_trees.common.Status.SUCCESS
        else:
            return py_trees.common.Status.FAILURE

class GoToBall(py_trees.behaviour.Behaviour):
    def __init__(self, robot: Robot):
        super().__init__(name="GoToBall")
        self.robot = robot

    def update(self):
        try:
            self.robot.goToBall()
            return py_trees.common.Status.SUCCESS
        except:
            return py_trees.common.Status.FAILURE

class StartDribbler(py_trees.behaviour.Behaviour):
    def __init__(self, robot: Robot):
        super().__init__(name="StartDribber")
        self.robot = robot

    def update(self):
        try:
            self.robot.startDribbler()
            return py_trees.common.Status.SUCCESS
        except:
            return py_trees.common.Status.FAILURE

class CanShoot(py_trees.behaviour.Behaviour):
    def __init__(self, robot: Robot):
        super().__init__(name="CanShoot")
        self.robot = robot

    def update(self):
        if self.robot.canShoot():
            return py_trees.common.Status.SUCCESS
        else:
            return py_trees.common.Status.FAILURE

class Shoot(py_trees.behaviour.Behaviour):
    def __init__(self, robot: Robot):
        super().__init__(name="Shoot")
        self.robot = robot

    def update(self):
        try:
            self.robot.shoot()
            return py_trees.common.Status.SUCCESS
        except:
            return py_trees.common.Status.FAILURE