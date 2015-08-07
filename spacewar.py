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
        self.mass = 30*1000
        self.fxcenter = 0.5
        self.fycenter = 0.5

class Vector(object):
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
    def mag(self):
        return math.sqrt(self.x*self.x + self.y*self.y)
    
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
        self.fxcenter = 0.5
        self.fycenter = 0.5
        
    def step(self):
        dt = 0.033
        R = Vector(self.sun.x-self.x, self.sun.y-self.y)
        Ur = R.unit()
        ag = GravitySprite.G*self.sun.mass/R.mag()**2
        Ag = Vector(Ur.x*ag, Ur.y*ag)
        vx = self.vx
        vy = self.vy
        self.vx += Ag.x * dt
        self.vy += Ag.y * dt
        self.x += self.vx + 0.5*Ag.x*dt*dt
        self.y += self.vy + 0.5*Ag.y*dt*dt

class Ship1(GravitySprite):
    
    asset = ImageAsset("four_spaceship_by_albertov.png", 
        Frame(227,0,292-227,92), 1)
        
    def __init__(self, position, velocity, sun):
        super().__init__(Ship1.asset, position, velocity, sun)
    
class Ship2(GravitySprite):
    
    asset = ImageAsset("four_spaceship_by_albertov.png", 
        Frame(0,0,86,92), 1)
        
    def __init__(self, position, velocity, sun):
        super().__init__(Ship2.asset, position, velocity, sun)
    
class Spacewar(App):
    
    def __init__(self, width, height):
        super().__init__(width, height)
        for x in range(width//Stars.width + 1):
            for y in range(height//Stars.height + 1):
                Stars((x*Stars.width, y*Stars.height))
        self.sun = Sun((width/2, height/2))
        self.ship1 = Ship1((width/2+100,height/2), (0,-4), self.sun)
        self.ship2 = Ship2((width/2-100,height/2), (0,4), self.sun)
        
    def step(self):
        #for ship in self.getSpritesbyClass(Ship1
        self.ship1.step()
        self.ship2.step()


app = Spacewar(1000,800)
app.run()

