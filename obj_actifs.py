from direct.actor.Actor import Actor
from panda3d.core import CollisionSphere, CollisionNode
from panda3d.core import BitMask32
from panda3d.core import Vec3

#Dépendances
from config import *

#=============================================
# classe représentant les objets participant au jeu
# Paramètres de init:
#    parent : instance de Game
#    pos : position initial de l'objet
#    modelName : chemin pour le modele
#    modelAnims : chemin pour les animations du modele
#    colliderName : nom pour les collisions
#    scale : Echelle de représentation
#=============================================

class Obj_actifs:
    def __init__(self,parent,pos,modelName, modelAnims,colliderName,scale):
        self.parent=parent
        self.pos_init=pos
        self.actor = Actor(modelName, modelAnims)
        self.actor.setPos(self.pos_init)
        self.colliderName=colliderName
        self.actor.setScale(scale)
        self.Init_coll()
        print(f" Objet : {self.colliderName} : init collisions")
        self.parent.base.pusher.addCollider(self.collider, self.actor)
        self.parent.base.cTrav.addCollider(self.collider, base.pusher)
 # ================================================================
 # Initialisation des collisions
 #
 #=================================================================
    def Init_coll(self):
        colliderNode = CollisionNode(self.colliderName)
        colliderNode.addSolid(CollisionSphere(0, 0, 0, 0.5))
        self.collider = self.actor.attachNewNode(colliderNode)
        self.collider.show()
        # masque collision
        mask = BitMask32()
        mask.setBit(2)
        mask.setBit(0)
        self.collider.node().setIntoCollideMask(mask)
        mask = BitMask32()
        mask.setBit(2)
        mask.setBit(1)
        self.collider.node().setFromCollideMask(mask)
        self.collider.setPythonTag("owner", self)

#=============================================
# classe représentant le heros du jeu 
# Paramètres de init:
#    parent : instance de Game
#    pos : position initial de l'objet
#    modelName : chemin pour le modele
#    modelAnims : chemin pour les animations du modele
#    -> maxHealth : etat de santé initial
#    -> maxSpeed : vitesse max de déplacement
#    colliderName : nom pour les collisions
#    scale : Echelle de représentation
#=============================================
        
        
class Heros(Obj_actifs):
    def __init__(self,parent,pos,modelName, modelAnims, maxHealth, maxSpeed,colliderName,scale):
        Obj_actifs.__init__(self,parent,pos,modelName, modelAnims,colliderName,scale)
        self.maxHealth = maxHealth
        self.health = maxHealth                    
        self.maxSpeed = maxSpeed
        self.velocity = Vec3(0, 0, 0)
        self.acceleration = ACCELERATION
        self.walking = False
        self.actor.loop("stand")
 # ================================================================
 # Gestion des mouvements du heros
 #
 #=================================================================        
    def update(self, keys, dt):
        self.update_velocity(dt)
        self.walking = False
        if keys["up"]:
            self.walking = True
            self.actor.getChild(0).setH(180)
            self.velocity.addY(self.acceleration*dt)
        if keys["down"]:
            self.walking = True
            self.actor.getChild(0).setH(0)
            self.velocity.addY(-self.acceleration*dt)
        if keys["left"]:
            self.walking = True
            self.actor.getChild(0).setH(270)
            self.velocity.addX(-self.acceleration*dt)
        if keys["right"]:
            self.walking = True
            self.actor.getChild(0).setH(90)
            self.velocity.addX(self.acceleration*dt)

        # controles des mvts
        if self.walking:
            standControl = self.actor.getAnimControl("stand")
            if standControl.isPlaying():
                standControl.stop()

            walkControl = self.actor.getAnimControl("walk")
            if not walkControl.isPlaying():
                self.actor.loop("walk")
        else:
            standControl = self.actor.getAnimControl("stand")
            if not standControl.isPlaying():
                self.actor.stop("walk")
                self.actor.loop("stand")

    def update_velocity(self, dt):
        # If we're going faster than our maximum speed,
        # set the velocity-vector's length to that maximum
        speed = self.velocity.length()
        if speed > self.maxSpeed:
            self.velocity.normalize()
            self.velocity *= self.maxSpeed
            speed = self.maxSpeed

        # If we're walking, don't worry about friction.
        # Otherwise, use friction to slow us down.
        if not self.walking:
            frictionVal = FRICTION*dt
            if frictionVal > speed:
                self.velocity.set(0, 0, 0)
            else:
                frictionVec = -self.velocity
                frictionVec.normalize()
                frictionVec *= frictionVal

                self.velocity += frictionVec

        # Move the character, using our velocity and
        # the time since the last update.
        self.actor.setPos(self.actor.getPos() + self.velocity*dt)
        
        
        