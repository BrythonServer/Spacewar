from ggame import App, Sprite, ImageAsset


class Stars(Sprite):

    asset = ImageAsset("starfield.jpg")

    def __init__(self, position):
        super().__init__(Stars.asset, position)

class Sun(Sprite):
    
    asset = ImageAsset("sun.png")
    
    def __init__(self, position):
        super().__init__(Sun.asset, position)
        
class Spacewar(App):
    
    def __init__(self, width, height):
        super().__init__(width, height)
        self.star1 = Stars((0,0))
        sun = Sun((400,300))
        sunw = sun.width
        sunh = sun.height
        print(sunw, sunh)
        #for x in range(width//sw + 1):
        #    for y in range(height//sh + 1):
        #        #print(x*sw, y*sh)
        #        Stars((x*sw, y*sh))
        #star1.destroy()
        
    def step(self):
        sw = self.star1.width
        sh = self.star1.height
        #star1.destroy()
        print(self.sw, self.sh)

app = Spacewar(800,600)
app.run()

