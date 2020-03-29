from direct.showbase.ShowBase import ShowBase

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
        
        
game = Game()
game.run()