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
        self.circularCollisionModel()

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
    T = 3.0
    
    def __init__(self, asset, position, velocity, sun):
        super().__init__(asset, position)
        self.vx = velocity[0]
        self.vy = velocity[1]
        self.sun = sun
        self.fxcenter = 0.5
        self.fycenter = 0.5
        self.rrate = 0.0
        self.thrust = 0.0
        
    def step(self):
        dt = 0.033
        R = Vector(self.sun.x-self.x, self.sun.y-self.y)
        Ur = R.unit()
        ag = GravitySprite.G*self.sun.mass/R.mag()**2
        Ag = Vector(Ur.x*ag, Ur.y*ag)
        vx = self.vx
        vy = self.vy
        self.vx += (Ag.x + self.thrust*GravitySprite.T*math.sin(self.rotation))* dt
        self.vy += (Ag.y - self.thrust*GravitySprite.T*math.cos(self.rotation))* dt
        self.x += self.vx + 0.5*Ag.x*dt*dt
        self.y += self.vy + 0.5*Ag.y*dt*dt


class Bullet(GravitySprite):
    
    asset = ImageAsset("blast.png", Frame(0,0,8,8), 8)
    
    def __init__(self, app, sun):
        super().__init__(Bullet.asset, (0,0), (0,0), sun)
        self.visible = False
        self.firing = False
        self.time = 0
        self.circularCollisionModel()
        
    def shoot(self, position, velocity, time):
        self.position = position
        self.vx = velocity[0]
        self.vy = velocity[1]
        self.time = time*30
        self.visible = True
        self.firing = True

    def step(self):
        if self.time > 0:
            self.time -= 1
            self.nextImage(True)
            super().step()
            if self.collidingWith(self.sun):
                self.visible = False
            ships = self.collidingWithSprites(Ship1).extend(self.collidingWithSprites(Ship2))
            if len(ships):
                if not self.firing:
                    ships[0].explode()
                self.visible = False
            elif self.firing:
                self.firing = False
                
        elif self.visible:
            self.visible = False
        
        

class Ship(GravitySprite):

    R = 2.0
    bullets = 2
    
    def __init__(self, asset, app, position, velocity, sun):
        self.bullets = []
        for i in range(Ship.bullets):
            self.bullets.append(Bullet(app, sun))
        super().__init__(asset, position, velocity, sun)
        self.initposition = position
        self.initvelocity = self.vx, self.vy
        self.app = app
        self.circularCollisionModel()

    def registerKeys(self, keys):
        commands = ["left", "right", "forward", "fire"]
        self.keymap = dict(zip(keys, commands))
        [self.app.listenKeyEvent("keydown", k, self.controldown) for k in keys]
        [self.app.listenKeyEvent("keyup", k, self.controlup) for k in keys]

    def shootvector(self):
        vel = 2
        xv = vel*math.sin(self.rotation)
        yv = vel*(-math.cos(self.rotation))
        return xv + self.vx, yv + self.vy
        

    def controldown(self, event):
        command = self.keymap[event.key]
        if command == "left":
            self.rrate = -0.01*Ship.R
        elif command == "right":
            self.rrate = Ship.R*0.01
        elif command == "forward":
            self.thrust = 0.1
        elif command == "fire":
            for bullet in self.bullets:
                if bullet.time == 0:
                    bullet.shoot(self.position, self.shootvector(), 15)
                    break
                        
            
    def controlup(self, event):
        command = self.keymap[event.key]
        if command in ["left", "right"]:
            self.rrate = 0.0
        elif command == "forward":
            self.thrust = 0.0
            
    def step(self):
        super().step()
        self.rotation += self.rrate
        for bullet in self.bullets:
            bullet.step()
        bullets = self.collidingWithSprites(Bullet)
        #for bullet in bullets:
        #    if bullet.visible:
        #        if self.collidingWith(bullet) and not bullet.firing:
        #                bullet.visible = False
        #                print("Hit by bullet!")
        #                self.explode()
        #        elif bullet.firing:
        #            bullet.firing = False
        if self.collidingWith(self.sun):
            self.explode()
            print("Hit the sun!")

    def explode(self):
        print("boom: ", type(self))
        self.reset()
        
    def reset(self):
        self.position = self.initposition
        self.vx, self.vy = self.initvelocity

            
class Ship1(Ship):
    
    asset = ImageAsset("four_spaceship_by_albertov.png", 
        Frame(227,0,292-227,92), 1)
        
    def __init__(self, app, position, velocity, sun):
        super().__init__(Ship1.asset, app, position, velocity, sun)
        self.registerKeys(["left arrow", "right arrow", "up arrow", "enter"])
        
    def step(self):
        super().step()
        collides = self.collidingWithSprites(Ship2)
        if len(collides):
            collides[0].explode()
            self.explode()
        
class Ship2(Ship):
    
    asset = ImageAsset("four_spaceship_by_albertov.png", 
        Frame(0,0,86,92), 1)
        
    def __init__(self, app, position, velocity, sun):
        super().__init__(Ship2.asset, app, position, velocity, sun)
        self.registerKeys(["a", "d", "w", "space"])

    def step(self):
        super().step()
        collides = self.collidingWithSprites(Ship1)
        if len(collides):
            collides[0].explode()
            self.explode()
    

class Spacewar(App):
    
    def __init__(self, width, height):
        super().__init__(width, height)
        for x in range(self.width//Stars.width + 1):
            for y in range(self.height//Stars.height + 1):
                Stars((x*Stars.width, y*Stars.height))
        self.sun = Sun((self.width/2, self.height/2))
        self.ship1 = Ship1(self, (self.width/2+100,self.height/2), (0,-4), self.sun)
        self.ship2 = Ship2(self, (self.width/2-100,self.height/2), (0,4), self.sun)
        
    def step(self):
        self.ship1.step()
        self.ship2.step()


app = Spacewar(0,0)
app.run()

