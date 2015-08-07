from ggame import App, Sprite, ImageAsset


class Stars(Sprite):

    asset = ImageAsset("starfield.jpg")

    def __init__(self, position):
        super().__init__(Stars.asset, position)

class Sun(Sprite):
    
    asset = ImageAsset("sun.png")
    
    def __init__(self, position):
        super().__init__(Sun.asset, 400,300)
        
class Spacewar(App):
    
    def __init__(self, width, height):
        super().__init__(width, height)
        star1 = Stars((0,0))
        sun = Sun()
        sw = star1.GFX.width
        sh = star1.GFX.height
        star1.destroy()
        print(sw, sh)
        sunw = sun.width
        sunh = sun.height
        print(sunw, sunh)
        #for x in range(width//sw + 1):
        #    for y in range(height//sh + 1):
        #        #print(x*sw, y*sh)
        #        Stars((x*sw, y*sh))
        #star1.destroy()
        
app = Spacewar(800,600)

