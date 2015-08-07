from ggame import App, Sprite, ImageAsset


class Stars(Sprite):

    starasset = ImageAsset("starfield.jpg")

    def __init__(self, position):
        super().__init__(Stars.starasset, position)
        
class Spacewar(App):
    
    def __init__(self, width, height):
        super().__init__(width, height)
        star1 = Stars((0,0))
        for x in range(1, width//Stars.starasset.width + 1):
            for y in range(1, height//Stars.starasset.height + 1):
                Stars((x*Stars.starasset.width, y*Stars.starasset.height))
        
Spacewar(800,600).run()
