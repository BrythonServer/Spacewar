from ggame import App, Sprite, ImageAsset


class Stars(Sprite):

    starasset = ImageAsset("starfield.jpg")

    def __init__(self, position):
        super().__init__(Stars.starasset, position)
        
class Spacewar(App):
    
    def __init__(self, width, height):
        super().__init__(width, height)
        star1 = Stars((0,0))
        star2 = Stars((512,0))
        star3 = Stars((0,512))
        star4 = Stars((512,512))
        
app = Spacewar(800,600)
app.run()
