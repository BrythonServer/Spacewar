from ggame import App, Sprite, ImageAsset, Frame, SoundAsset, Sound
import math
from time import time

class Stars(Sprite):

    asset = ImageAsset("images/starfield.jpg")
    width = 512
    height = 512

    def __init__(self, position):
        super().__init__(Stars.asset, position)

class Sun(Sprite):
    
    asset = ImageAsset("images/sun.png")
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
    
    G = 50.0

    def __init__(self, asset, position, velocity, sun):
        super().__init__(asset, position)
        self.vx = velocity[0]
        self.vy = velocity[1]
        self.sun = sun
        self.fxcenter = 0.5
        self.fycenter = 0.5
        self.rrate = 0.0
        self.thrust = 0.0
        self.mass = 1.0
        
    def step(self, T, dT):
        #dt = 0.033
        R = Vector(self.sun.x-self.x, self.sun.y-self.y)
        #Ur = R.unit()
        r = R.mag()
        Ux, Uy = R.x/r, R.y/r
        ag = GravitySprite.G*self.sun.mass/R.mag()**2
        Agx, Agy = Ux*ag, Uy*ag
        vx, vy = self.vx, self.vy
        At = self.thrust/self.mass
        dt2o2 = dT*dT*0.5
        self.vx += (Agx + At*math.sin(self.rotation))* dT
        self.vy += (Agy - At*math.cos(self.rotation))* dT
        self.x += self.vx * dT + Agx*dt2o2
        self.y += self.vy * dT + Agy*dt2o2


class Bullet(GravitySprite):
    
    asset = ImageAsset("images/blast.png", Frame(0,0,8,8), 8)
    pewasset = SoundAsset("sounds/pew1.mp3")
    
    def __init__(self, app, sun):
        super().__init__(Bullet.asset, (0,0), (0,0), sun)
        self.visible = False
        self.firing = False
        self.time = 0
        self.circularCollisionModel()
        self.pew = Sound(Bullet.pewasset)
        self.pew.volume = 10
        
    def shoot(self, position, velocity, time):
        self.position = position
        self.vx = velocity[0]
        self.vy = velocity[1]
        self.time = time
        self.visible = True
        self.firing = True
        self.pew.play()

    def step(self, T, dT):
        if self.time > 0:
            self.time -= dT
            if self.visible:
                self.nextImage(True)
                super().step(T, dT)
                if self.collidingWith(self.sun):
                    self.visible = False
                    ExplosionSmall(self.position)
                ships = []
                ships = self.collidingWithSprites(Ship1)
                ships.extend(self.collidingWithSprites(Ship2))
                if len(ships):
                    if not self.firing:
                        ships[0].explode()
                        self.visible = False
                elif self.firing:
                    self.firing = False
            
                
        else:
            if self.visible:
                self.visible = False
            self.time = 0


        
        

class Ship(GravitySprite):

    R = 2.0
    bullets = 2
    reappearasset = SoundAsset("sounds/reappear.mp3")
    
    def __init__(self, asset, app, position, velocity, sun):
        self.bullets = []
        for i in range(Ship.bullets):
            self.bullets.append(Bullet(app, sun))
        super().__init__(asset, position, velocity, sun)
        self.initposition = position
        self.initvelocity = self.vx, self.vy
        self.initrotation = self.rotation
        self.app = app
        self.mass = 1.0
        self.circularCollisionModel()
        self.imagex = 0
        self.reappear = Sound(Ship.reappearasset)
        self.reappear.volume = 40
        self.waitspawn = 0
        self.respawnplayed = False

    def registerKeys(self, keys):
        commands = ["left", "right", "forward", "fire"]
        self.keymap = dict(zip(keys, commands))
        [self.app.listenKeyEvent("keydown", k, self.controldown) for k in keys]
        [self.app.listenKeyEvent("keyup", k, self.controlup) for k in keys]

    def shootvector(self):
        vel = 150
        xv = vel*math.sin(self.rotation)
        yv = vel*(-math.cos(self.rotation))
        return xv + self.vx, yv + self.vy
        

    def controldown(self, event):
        if self.visible:
            command = self.keymap[event.key]
            if command == "left":
                self.rrate = -Ship.R
            elif command == "right":
                self.rrate = Ship.R
            elif command == "forward":
                self.thrust = 40.0
                self.imagex = 1 # start the animated rockets
                self.setImage(self.imagex)
            elif command == "fire":
                for bullet in self.bullets:
                    if bullet.time == 0:
                        bullet.shoot(self.position, self.shootvector(), 10)
                        break
                        
            
    def controlup(self, event):
        command = self.keymap[event.key]
        if command in ["left", "right"]:
            self.rrate = 0.0
        elif command == "forward":
            self.thrust = 0.0
            self.imagex = 0 # stop the animated rockets
            self.setImage(self.imagex)
            
    def step(self, T, dT):
        if self.waitspawn > 0:
            self.waitspawn -= dT
            if self.waitspawn < 1 and not self.respawnplayed:
                self.reappear.play()
                self.respawnplayed = True
            if self.waitspawn <= 0:
                self.reset()
        if self.visible:
            super().step(T, dT)
            self.rotation += self.rrate * dT
            for bullet in self.bullets:
                bullet.step(T, dT)
            if self.collidingWith(self.sun):
                self.explode()
            if self.thrust != 0.0:
                self.imagex += 1    # animate the rockets
                if self.imagex == 4:
                    self.imagex = 1
                self.setImage(self.imagex)
            if (self.x < -100 or self.x > self.app.width + 100 or
                self.y < -100 or self.y > self.app.height + 100):
                self.explode()
        

    def explode(self):
        self.visible = False
        ExplosionBig(self.position)
        self.position = self.initposition
        self.vx, self.vy = self.initvelocity
        self.rotation = self.initrotation
        self.waitspawn = 5

    def reset(self):
        self.visible = True
        self.respawnplayed = False


            
class Ship1(Ship):
    
    asset = ImageAsset("images/four_spaceship_by_albertov_with_thrust.png", 
        Frame(227,0,292-227,125), 4, 'vertical')
        
    def __init__(self, app, position, velocity, sun):
        super().__init__(Ship1.asset, app, position, velocity, sun)
        self.registerKeys(["left arrow", "right arrow", "up arrow", "enter"])
        
    def step(self, T, dT):
        super().step(T, dT)
        if self.visible:
            collides = self.collidingWithSprites(Ship2)
            if len(collides):
                if collides[0].visible:
                    collides[0].explode()
                    self.explode()
        
class Ship2(Ship):
    
    asset = ImageAsset("images/four_spaceship_by_albertov_with_thrust.png", 
        Frame(0,0,86,125), 4, 'vertical')
        
    def __init__(self, app, position, velocity, sun):
        super().__init__(Ship2.asset, app, position, velocity, sun)
        self.registerKeys(["a", "d", "w", "space"])

    def step(self, T, dT):
        super().step(T, dT)
        if self.visible:
            collides = self.collidingWithSprites(Ship1)
            if len(collides):
                if collides[0].visible:
                    collides[0].explode()
                    self.explode()

class ExplosionSmall(Sprite):
    
    asset = ImageAsset("images/explosion1.png", Frame(0,0,128,128), 10)
    boomasset = SoundAsset("sounds/explosion1.mp3")
    
    def __init__(self, position):
        super().__init__(ExplosionSmall.asset, position)
        self.image = 0
        self.center = (0.5, 0.5)
        self.boom = Sound(ExplosionSmall.boomasset)
        self.boom.play()
        
    def step(self):
        self.setImage(self.image//2)  # slow it down
        self.image += 1
        if self.image == 20:
            self.destroy()

class ExplosionBig(Sprite):
    
    asset = ImageAsset("images/explosion2.png", Frame(0,0,4800/25,195), 25)
    boomasset = SoundAsset("sounds/explosion2.mp3")
    
    def __init__(self, position):
        super().__init__(ExplosionBig.asset, position)
        self.image = 0
        self.center = (0.5, 0.5)
        self.boom = Sound(ExplosionBig.boomasset)
        self.boom.play()
        
    def step(self):
        self.setImage(self.image//2)  # slow it down
        self.image += 1
        if self.image == 50:
            self.destroy()

class Spacewar(App):
    
    def __init__(self, width, height):
        super().__init__(width, height)
        for x in range(self.width//Stars.width + 1):
            for y in range(self.height//Stars.height + 1):
                Stars((x*Stars.width, y*Stars.height))
        self.sun = Sun((self.width/2, self.height/2))
        self.ship1 = Ship1(self, (self.width/2+140,self.height/2), (0,-120), self.sun)
        self.ship2 = Ship2(self, (self.width/2-140,self.height/2), (0,120), self.sun)
        self.Tlast = time()
        
    def step(self):
        T = time()
        dT = T-self.Tlast
        self.Tlast = T
        self.ship1.step(T, dT)
        self.ship2.step(T, dT)
        explosions = self.getSpritesbyClass(ExplosionSmall)
        for explosion in explosions:
            explosion.step()
        explosions = self.getSpritesbyClass(ExplosionBig)
        for explosion in explosions:
            explosion.step()

app = Spacewar(0,0)
app.run()

