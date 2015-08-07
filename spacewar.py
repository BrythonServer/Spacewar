from ggame import App, Sprite, ImageAsset


class Stars(Sprite):

    starasset = ImageAsset("starfield.jpg")

    def __init__(self, position):
        super().__init__(Stars.starasset, position)
        
class Spacewar(App):
    
    def __init__(self, width, height):
        super().__init__(width, height)
        for x in range(width//Stars.starasset.width + 1):
            for y in range(height//Stars.starasset.height + 1):
                Stars((x*Stars.starasset.width, y*Stars.starasset.height))
        
Spacewar(800,600).run()
