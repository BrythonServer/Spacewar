from ggame import App, Sprite, ImageAsset, Frame
import math


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
        self.mass = 1000

class Vector(object):
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
    def mag(self):
        return math.sqrt(x**2 + y**2)
    
    def unit(self):
        r = self.mag()
        if r == 0:
            return Vector(0,0)
        else:
            return Vector(self.x/r, self.y/r)

class GravitySprite(Sprite):
    
    G = 1.0
    
    def __init__(self, asset, position, velocity, sun):
        super().__init__(asset, position)
        self.vx = velocity[0]
        self.vy = velocity[1]
        self.sun = sun
        
    def step(self):
        R = Vector(self.sun.x-self.x, self.sun.y-self.y)
        Ur = R.unit()
        ag = Gravity.G*sun.mass/R.mag()**2
        Ag = Vector(Ur.x*ag, Ur.y*ag)
        self.x += self.vx
        self.y += self.vy
        self.vx += Ag.x
        self.vy ++ Ag.y
        

class Ship1(GravitySprite):
    
    # ship is at 227,0 pixels
    width = 292-227
    height = 92
    asset = ImageAsset("four_spaceship_by_albertov.png", 
        Frame(227,0,292-227,92), 1)
        
    def __init__(self, position, velocity, sun):
        super().__init__(Ship1.asset, position, velocity, sun)
    
class Spacewar(App):
    
    def __init__(self, width, height):
        super().__init__(width, height)
        for x in range(width//Stars.width + 1):
            for y in range(height//Stars.height + 1):
                Stars((x*Stars.width, y*Stars.height))
        self.sun = Sun((width/2 - Sun.width/2, height/2 - Sun.height/2))
        self.ship1 = Ship1((500,300), (0,-5), self.sun)
        
    def step(self):
        #for ship in self.getSpritesbyClass(Ship1
        self.ship1.step()


app = Spacewar(800,600)
app.run()

