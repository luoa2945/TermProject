import module_manager
module_manager.review()
import pygame

class Player(object):
    def __init__(self, winW, winH, w, h, groundH):
        #dimensions
        self.screenW, self.screenH = winW, winH
        self.radius = 50 #image radius for scaling
        self.w, self.h = w, h
        self.groundH = groundH
        
        #player position
        self.x = winW/2
        self.y = winH - groundH - self.h/2
        self.xVel = 10 #x velocity
        self.yVel = 10 #y velocity
        self.charBox = (self.x-self.w*self.radius/2, 
            self.y-self.h*self.radius/2, self.w, self.h)
        
        #upload images
        self.standing = pygame.image.load('stand.png')
        self.jump = pygame.image.load('jump.png')
        self.walk = [pygame.image.load('walk_1.png'), 
        self.standing, pygame.image.load('walk_2.png'), self.standing]
        self.firing = pygame.image.load('firing.png')
        
        #character state
        self.jumpCount = 10 #jump height
        self.isJump = False
        self.dir = "Right"
        self.onPlatform = False
        self.walkCount = 0
        self.isWalk = False
        self.isJumping = False
        self.isFiring = False
    
    #draw character graphics
    def drawChar(self, window):
        #red hitbox for sensing
        pygame.draw.rect(window, (255,0,0), 
            (int(self.x)-self.w/2, int(self.y) - self.groundH, 
            self.w ,self.h), 2)
        #jump image
        if self.isJump:
            if self.dir == "Left":
                self.char = pygame.transform.flip(self.jump, True, False)
            else: self.char = self.jump
        #walk image
        elif self.isWalk: self.char = self.walk[self.walkCount % 4]
        #standing image
        else: 
            self.char = self.standing
            #firing image
            if self.isFiring: self.char = self.firing 
               
        #transform scale by square radius
        self.char = pygame.transform.scale(self.char, 
            (self.radius*2,self.radius*2))
        #draw character on window
        window.blit(self.char, 
        (self.x -self.radius, self.y - self.groundH))
        
        
    def moveLeft(self, platforms):
        #check touching left wall
        if self.x - self.w/2 <= 0: 
            self.x += self.xVel
        #move left
        self.x -= self.xVel 
        #if falling off platform
        if not self.isJump: self.checkFall(platforms) 
        
    def moveRight(self, platforms): 
        #check touching right wall
        if self.x + self.w/2 >= self.screenW: 
            self.x -= self.xVel
        #move right
        self.x += self.xVel
        #check if falling off platfrom
        if not self.isJump: self.checkFall(platforms)
    
    #move left or right
    def move(self, dir, platforms):
        self.isWalk = True
        self.dir = dir
        self.walkCount += 1
        if dir == "Left": self.moveLeft(platforms)
        else: self.moveRight(platforms)
    
    #cat jump
    def jumpUp(self, platforms):
        if self.jumpCount >= -self.yVel:
            neg = 1 #pos velocity
            if self.jumpCount < 0: #reached peak
                neg = -1 #neg velocity
                
            newY = -(self.jumpCount ** 2) * 0.5 * neg
            #if not colliding with anything
            if not self.collision(platforms, (0,newY)):
                #jump
                self.y -= (self.jumpCount ** 2) * 0.5 * neg
                self.jumpCount -= 1
            else:
                #stop jumping, reset max jumpCount
                self.isJump = False
                self.jumpCount = self.yVel
        else:
            #stop jumping
            self.isJump = False
            self.jumpCount = self.yVel
            #see if player is in midair
            self.checkFall(platforms)
    
    #see if player should continue falling        
    def checkFall(self, platforms):
        fall = True
        for platform in platforms:
            #if on platform don't fall
            if platform.x - platform.w/2 - self.w/2 < self.x and \
            self.x < platform.x + platform.w/2 + self.w/2 and \
                self.y < platform.y + platform.h/2 + self.h/2:
                fall = False
                self.y = platform.y - platform.h/2 - self.h/2
                
        #fall if not on any platform
        if (fall): 
            self.fall()
    
    #fall to ground
    def fall(self):
        self.onPlatform = False
        while (self.y < self.screenH - self.groundH - self.h/2):
            self.y += 1
        #place on ground
        self.y = self.screenH - self.groundH - self.h/2
    
    #check if colliding with platforms
    def collision(self, platforms, dir):
        #dir stored as tuple (x dir, y dir)
        newX = self.x + dir[0]
        newY = self.y + dir[1]
        for platform in platforms:
            #if collided with platform
            if platform.x - platform.w/2 - self.w/2 < newX and \
            newX < platform.x + platform.w/2 + self.w/2 and \
            platform.y - platform.h/2 - self.h/2 < newY and \
                newY < platform.y + platform.h/2 + self.h/2 :
            
                #if jumped onto platform
                if self.isJump and self.y < \
                platform.y - platform.h/2 - self.h/2:
                    self.y = platform.y - platform.h/2 - self.h/2
                    self.onPlatform = True
                    
                #if hit below platform
                elif self.isJump and self.y > \
                platform.y + platform.h/2 + self.h/2:
                    #fall down
                    self.onPlatform = False
                    self.fall()
                        
                return True
        return False
        
        
        
        
        
        
     