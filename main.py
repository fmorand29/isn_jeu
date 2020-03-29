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

#Dépendances
from config import *

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
        #self.heros.update(self.keyMap, dt)
        #self.tempEnemy.update(self.player, dt)
        return task.cont
        
game = Game()
game.run()