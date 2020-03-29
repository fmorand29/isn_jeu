from panda3d.core import CollisionRay, CollisionHandlerQueue
from panda3d.core import CollisionSphere, CollisionNode
from panda3d.core import BitMask32


class Arme:
    def __init__(self,parent):
        self.parent=parent
    


class Boule_feu(Arme):
    def __init__(self,parent):
        Arme.__init__(self,parent)
        # init du rayon de la mort
        self.ray = CollisionRay(0, 0, 0, 0, 1, 0)
        rayNode = CollisionNode("boule_feu")
        rayNode.addSolid(self.ray)
        mask = BitMask32()
        mask.setBit(2)
        rayNode.setFromCollideMask(mask)
        maskI = BitMask32()
        maskI.setBit(0)
        rayNode.setIntoCollideMask(maskI)
        self.rayNodePath = render.attachNewNode(rayNode)
        self.rayQueue = CollisionHandlerQueue()
        self.parent.base.cTrav.addCollider(self.rayNodePath, self.rayQueue)
        self.ray.setOrigin(12, 9, 7)
        self.ray.setDirection(self.parent.heros.actor.getPos()-self.parent.sorcier.obj.getPos())
        self.rayNodePath.show()
        
    def update(self,keys, dt):
        self.ray.setDirection(self.parent.heros.actor.getPos()-self.parent.sorcier.obj.getPos())
        if self.rayQueue.getNumEntries() > 0:
            self.rayQueue.sortEntries()
            rayHit = self.rayQueue.getEntry(0)
            hitPos = rayHit.getSurfacePoint(render)
            hitNodePath = rayHit.getIntoNodePath()
            print (hitNodePath)
        