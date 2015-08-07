from ggame import App, Sprite, ImageAsset

class Stars(Sprite):
    
    def __init__(self, position):
        super().__init__(ImageAsset("starfield.jpg"), position)
        
class Spacewar(App):
    
    def __init__(self, width, height):
        super().__init__(width, height)
        self.stars = Stars((0,0))
        
Spacewar(800,600).run()
