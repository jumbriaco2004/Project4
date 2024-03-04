from direct.task import Task
from panda3d.core import *
from direct.showbase.ShowBase import ShowBase
from CollideObjectBase import *

class Universe(InverseSphereCollideObject):
    def __init__(self, loader: Loader, modelPath: str, parentNode: NodePath, nodeName: str, texPath: str, posVec: Vec3, scaleVec: float):
        super(Universe, self).__init__(loader, modelPath, parentNode, nodeName, Vec3(0, 0, 0), 15000)
        self.modelNode = loader.loadModel(modelPath)
        self.modelNode.reparentTo(parentNode)
        self.modelNode.setPos(posVec)
        self.modelNode.setScale(scaleVec)

        self.modelNode.setName(nodeName)
        tex = loader.loadTexture(texPath)
        self.modelNode.setTexture(tex, 1)

class Planet(SphereCollideObject):
    def __init__(self, loader: Loader, modelPath: str, parentNode: NodePath, nodeName: str, texPath: str, posVec: Vec3, scaleVec: float):
        super(Planet, self).__init__(loader, modelPath, parentNode, nodeName, Vec3(0, 0, 0), 1)
        self.modelNode = loader.loadModel(modelPath)
        self.modelNode.reparentTo(parentNode)
        self.modelNode.setPos(posVec)
        self.modelNode.setScale(scaleVec)

        self.collisionNode = self.modelNode.attachNewNode(CollisionNode(nodeName + "_cNode"))
        self.collisionNode.node().addSolid(CollisionSphere(Vec3(0, 0, 0), 1))
        self.collisionNode.show()

        self.modelNode.setName(nodeName)
        tex = loader.loadTexture(texPath)
        self.modelNode.setTexture(tex, 1)

class SpaceStation(CapsuleCollidableObject):
    def __init__(self, loader: Loader, modelPath: str, parentNode: NodePath, nodeName: str, posVec: Vec3, Hpr: Vec3 , scaleVec: float):
        super(SpaceStation, self).__init__(loader, modelPath, parentNode, nodeName, 1, -1, 5, 1, -1, -5, 10)
        self.modelNode = loader.loadModel(modelPath)
        self.modelNode.reparentTo(parentNode)
        self.modelNode.setPos(posVec)
        self.modelNode.setHpr(Hpr)
        self.modelNode.setScale(scaleVec)
        self.modelNode.setName(nodeName)

        self.collisionNode = self.modelNode.attachNewNode(CollisionNode(nodeName + "_cNode"))
        self.collisionNode.node().addSolid(CollisionCapsule(1, -1, 5, 1, -1, -5, 10))
        self.collisionNode.show()
        
class Player(SphereCollideObject):
    def __init__(self, loader: Loader, modelPath: str, parentNode: NodePath, nodeName: str, texPath: str, posVec: Vec3, scaleVec: float, taskMgr, render, accept):
        super(Player, self).__init__(loader, modelPath, parentNode, nodeName, Vec3(0, 0, 0), 20) #Changes radius value of drone
        self.modelNode = loader.loadModel(modelPath)
        self.modelNode.reparentTo(parentNode)
        self.modelNode.setPos(posVec)
        self.modelNode.setScale(scaleVec)

        self.modelNode.setName(nodeName)
        tex = loader.loadTexture(texPath)
        self.modelNode.setTexture(tex, 1)

        self.collisionNode = self.modelNode.attachNewNode(CollisionNode(nodeName + "_cNode"))
        self.collisionNode.node().addSolid(CollisionSphere(Vec3(0, 0, 0), 20))
        self.collisionNode.show()

        self.taskMgr = taskMgr
        self.render = render
        self.accept = accept

        self.SetKeyBindings()
        
    def SetKeyBindings(self):
        self.accept("space", self.Thrust, [1])
        self.accept("space-up", self.Thrust, [0])
        self.accept("a", self.LeftTurn, [1])
        self.accept("a-up", self.LeftTurn, [0])
        self.accept("d", self.RightTurn, [1])
        self.accept("d-up", self.RightTurn, [0])
        self.accept("w", self.UpTurn, [1])
        self.accept("w-up", self.UpTurn, [0])
        self.accept("s", self.DownTurn, [1])
        self.accept("s-up", self.DownTurn, [0])
        self.accept("e", self.RightRoll, [1])
        self.accept("e-up", self.RightRoll, [0])
        self.accept("q", self.LeftRoll, [1])
        self.accept("q-up", self.LeftRoll, [0])

    #Thrust
    def Thrust(self, keyDown):
        if keyDown:
            self.taskMgr.add(self.ApplyThrust, "forward-thrust")
        else:
            self.taskMgr.remove("forward-thrust")

    def ApplyThrust(self, task):
        rate = 5
        trajectory = self.render.getRelativeVector(self.modelNode, Vec3.forward())
        trajectory.normalize()
        self.modelNode.setFluidPos(self.modelNode.getPos() + trajectory * rate)
        return Task.cont
    
    # H(eading).P(itch).R(oll)
    #Left Turn (H)
    def LeftTurn(self, keyDown):
        if keyDown:
            self.taskMgr.add(self.ApplyLeftTurn, "left-turn")
        else:
            self.taskMgr.remove("left-turn")

    def ApplyLeftTurn(self, task):
        rate = .5
        self.modelNode.setH(self.modelNode.getH() + rate)
        return Task.cont
    
    #Right Turn (H_)
    def RightTurn(self, keyDown):
        if keyDown:
            self.taskMgr.add(self.ApplyRightTurn, "right-turn")
        else:
            self.taskMgr.remove("right-turn")

    def ApplyRightTurn(self, task):
        rate = .5
        self.modelNode.setH(self.modelNode.getH() - rate)
        return Task.cont
    
    #Up Turn (P)
    def UpTurn(self, keyDown):
        if keyDown:
            self.taskMgr.add(self.ApplyUpTurn, "up-turn")
        else:
            self.taskMgr.remove("up-turn")

    def ApplyUpTurn(self, task):
        rate = .5
        self.modelNode.setP(self.modelNode.getP() + rate)
        return Task.cont
    
    #Down Turn (P)
    def DownTurn(self, keyDown):
        if keyDown:
            self.taskMgr.add(self.ApplyDownTurn, "down-turn")
        else:
            self.taskMgr.remove("down-turn")

    def ApplyDownTurn(self, task):
        rate = .5
        self.modelNode.setP(self.modelNode.getP() - rate)
        return Task.cont
    
    #Right Roll
    def RightRoll(self, keyDown):
        if keyDown:
            self.taskMgr.add(self.ApplyRightRoll, "right-roll")
        else:
            self.taskMgr.remove("right-roll")

    def ApplyRightRoll(self, task):
        rate = .5
        self.modelNode.setR(self.modelNode.getR() + rate)
        return Task.cont
    
        #Left Roll
    def LeftRoll(self, keyDown):
        if keyDown:
            self.taskMgr.add(self.ApplyLeftRoll, "left-roll")
        else:
            self.taskMgr.remove("left-roll")

    def ApplyLeftRoll(self, task):
        rate = .5
        self.modelNode.setR(self.modelNode.getR() - rate)
        return Task.cont  

class Drone(SphereCollideObject):
    droneCount = 0
    def __init__(self, loader: Loader, modelPath: str, parentNode: NodePath, nodeName: str, texPath: str, posVec: Vec3, scaleVec: float):
        super(Drone, self).__init__(loader, modelPath, parentNode, nodeName, Vec3(0, 0, 0), 10)
        self.modelNode = loader.loadModel(modelPath)
        self.modelNode.reparentTo(parentNode)
        self.modelNode.setPos(posVec)
        self.modelNode.setScale(scaleVec)

        self.modelNode.setName(nodeName)
        tex = loader.loadTexture(texPath)
        self.modelNode.setTexture(tex, 1)