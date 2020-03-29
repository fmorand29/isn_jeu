

class obj_inactifs:
    def __init__(self,pos,modelName,angle,Name,scale):
        self.pos_init=pos
        self.name=Name
        print("Init de ",self.name)
        self.obj=loader.loadModel(modelName)
        self.obj.getChild(0).setH(angle)
        self.obj.setPos(self.pos_init)
        self.obj.setScale(scale)
    