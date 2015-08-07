from ggame import App, Sprite, ImageAsset


class Stars(Sprite):

    starasset = ImageAsset("starfield.jpg")

    def __init__(self, position):
        super().__init__(Stars.starasset, position)
        
class Spacewar(App):
    
    def __init__(self, width, height):
        super().__init__(width, height)
        star1 = Stars((0,0))
        sw = star1.width
        sh = star1.height
        for x in range(width//sw + 1):
            for y in range(height//sh + 1):
                print(x*sw, y*sh)
                #Stars((x*sw, y*sh))
        #star1.destroy()
        
Spacewar(800,600)
