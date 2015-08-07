from ggame import App, Sprite, ImageAsset


class Stars(Sprite):

    asset = ImageAsset("starfield.jpg")
    width = 512
    height = 512

    def __init__(self, position):
        super().__init__(Stars.asset, position)

class Sun(Sprite):
    
    asset = ImageAsset("sun.png")
    width = 80
    height = 76
    
    def __init__(self, position):
        super().__init__(Sun.asset, position)
        
class Spacewar(App):
    
    def __init__(self, width, height):
        super().__init__(width, height)
        for x in range(width//Stars.width + 1):
            for y in range(height//Stars.height + 1):
                Stars((x*Stars.width, y*Stars.height))
        sun = Sun((width/2 - Sun.width/2, height/2 - Sun.height/2))

        
    def step(self):
        pass
    
app = Spacewar(800,600)
app.run()

