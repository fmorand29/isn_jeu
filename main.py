#==========================
# Auteur : FM
# 28/03/2020
#==========================

from direct.showbase.ShowBase import ShowBase
from panda3d.core import AmbientLight
from panda3d.core import DirectionalLight
from panda3d.core import Vec4, Vec3
from panda3d.core import CollisionTraverser
from panda3d.core import CollisionHandlerPusher
from panda3d.core import CollisionTube

#Dépendances
from config import *
from obj_actifs import *
from obj_inactifs import *

class Game(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.keyMap = {
            "up" : False,
            "down" : False,
            "left" : False,
            "right" : False,
            "shoot" : False
                        }
        self.base=base
        base.setFrameRateMeter(True)  # mesure le FPS
        # Création du plateau de jeu
        self.environment = loader.loadModel("./Environment/environment")
        self.environment.reparentTo(render)
        # Positionnement de la caméra
        self.Cam_init()
        # Réglages des éclairages
        self.ambientLight = AmbientLight("ambient light")
        self.Init_eclairage()
        # Gestions des collisions avec les autres objets (MUR pour l'instant)
        self.pusher = CollisionHandlerPusher()
        # Pour la gestion de l'arbre de collisions
        base.cTrav = CollisionTraverser()
        # gestion des déplacements
        self.Init_mvt()
        
        # création du heros selon le modele ./fox/Fox
        self.heros=Heros(self,Vec3(0, 0, 0),"./fox/Fox",
                              {
                                  "stand" : "./fox/Fox-Idle_fp",
                                  "walk" : "./fox/Fox-Walk_fp"
                              },
                            5,
                            10,"HEROS",2)
        self.heros.actor.reparentTo(render)
        # création des objets de décors
        self.tour1=obj_inactifs(Vec3(12, 9, 1),"tour/tour",0,"T1",1)
        self.tour1.obj.reparentTo(render)
        self.tour2=obj_inactifs(Vec3(-12, 9, 1),"tour/tour",0,"T2",1)
        self.tour2.obj.reparentTo(render)
        self.sorcier=obj_inactifs(Vec3(12, 9, 6),"sorcier/wizard",130,"SORCIER",0.45)
        self.sorcier.obj.reparentTo(render)
        
        # initialisation des déplacements
        self.Init_mvt()
        # initialisation des zones de collisions du decor
        self.Init_coll()
        # activation des évènements
        self.updateTask = taskMgr.add(self.update, "update")
        
        
    def Init_eclairage(self):
        
        self.ambientLight.setColor(Vec4(0.2, 0.2, 0.2, 1))
        self.ambientLightNodePath = render.attachNewNode(self.ambientLight)
        render.setLight(self.ambientLightNodePath)
        mainLight = DirectionalLight("main light")
        self.mainLightNodePath = render.attachNewNode(mainLight)
        # Turn it around by 45 degrees, and tilt it down by 45 degrees
        self.mainLightNodePath.setHpr(45, -45, 0)
        render.setLight(self.mainLightNodePath)
        render.setShaderAuto()        
#================================================================        
# réglage de la caméra
#================================================================   
    def Cam_init(self):
        self.cam.setPos(0, -25, 36)
        self.cam.lookAt(0,5,0)
#================================================================        
# réglage des mvts
#================================================================          
    def Init_mvt(self):
        self.accept("arrow_up", self.updateKeyMap, ["up", True])
        self.accept("arrow_up-up", self.updateKeyMap, ["up", False])
        self.accept("arrow_down", self.updateKeyMap, ["down", True])
        self.accept("arrow_down-up", self.updateKeyMap, ["down", False])
        self.accept("arrow_left", self.updateKeyMap, ["left", True])
        self.accept("arrow_left-up", self.updateKeyMap, ["left", False])
        self.accept("arrow_right", self.updateKeyMap, ["right", True])
        self.accept("arrow_right-up", self.updateKeyMap, ["right", False])
        self.accept("space", self.updateKeyMap, ["shoot", True])
        self.accept("space-up", self.updateKeyMap, ["shoot", False])
#================================================================        
# Création des zones de collisions pour le décor
# 4 murs
# TODO : A améliorer algorithmiquement
#================================================================            
    def Init_coll(self):
        wallSolid = CollisionTube(-8.0, 0, 0, 8.0, 0, 0, 0.2)
        wallNode = CollisionNode("MUR")
        wallNode.addSolid(wallSolid)
        wall = render.attachNewNode(wallNode)
        wall.setY(8.0)
        wall.show()
        wallSolid = CollisionTube(-8.0, 0, 0, 8.0, 0, 0, 0.2)
        wallNode = CollisionNode("MUR")
        wallNode.addSolid(wallSolid)
        wall = render.attachNewNode(wallNode)
        wall.setY(-8.0)
        wall.show()
        wallSolid = CollisionTube(0, -8.0, 0, 0, 8.0, 0, 0.2)
        wallNode = CollisionNode("MUR")
        wallNode.addSolid(wallSolid)
        wall = render.attachNewNode(wallNode)
        wall.setX(8.0)
        wall.show()
        wallSolid = CollisionTube(0, -8.0, 0, 0, 8.0, 0, 0.2)
        wallNode = CollisionNode("MUR")
        wallNode.addSolid(wallSolid)
        wall = render.attachNewNode(wallNode)
        wall.setX(-8.0)
        wall.show()
#================================================================        
# gestionnaire des evénements joueur
#================================================================            
    def updateKeyMap(self, controlName, controlState):
        self.keyMap[controlName] = controlState
        print (controlName, "mis a", controlState)
#================================================================        
# boucle d'activités
#================================================================  
    def update(self, task):
    # Pour chaque unité de temps
        dt = globalClock.getDt()
        self.heros.update(self.keyMap, dt)
        #self.tempEnemy.update(self.player, dt)
        return task.cont
        
game = Game()
game.run()