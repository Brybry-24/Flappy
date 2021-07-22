import pygame
from pygame.locals import *
import random

pygame.init()

clock = pygame.time.Clock()
fps = 60

screen_width = 750
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Furappu Bird')

# define font

font = pygame.font.SysFont('Bauhaus 93', 60)

# define color

aoba = (104,71,141)


# define game variable
 
ground_move = 0
move_speed = 4
flying = False
game_over = False
pipe_gap = 150
pipe_frequency = 1500 #milsec
last_pipe = pygame.time.get_ticks() - pipe_frequency
score = 0
pass_pipe = False

#load images

bg = pygame.image.load('img/bg.png')
ground = pygame.image.load('img/ground.png')
button_img = pygame.image.load('img/restart.png')

def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img,(x,y))

def reset_game():
    pipe_group.empty()
    birdy.rect.x = 100
    birdy.rect.y = int(screen_height / 2)
    score = 0
    return score


class Bird(pygame.sprite.Sprite):
    def __init__(self, x , y):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.index = 0
        self.counter = 0
        for num in range(1, 4):
            img = pygame.image.load(f'img/bird{num}.png')
            self.images.append(img)
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.vel = 0
        self.clicked = False

    def update(self):
        
        if flying == True:
            # gravity
            self.vel += 0.5
            if self.vel > 8:
                self.vel = 8
           
            if self.rect.bottom < 480:
                self.rect.y += int(self.vel)
                    
        if game_over == False:
            
            #jump
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                self.vel = -10
            if pygame.mouse.get_pressed()[0] == 0 and self.clicked == True:
                self.clicked = False

            # ANIMATION
            self.counter += 1
            flap_cooldown = 5

            if self.counter > flap_cooldown:
                self.counter = 0
                self.index += 1
            if  self.index >= len(self.images):
                self.index = 0
            self.image = self.images[self.index]
            

            #rotate bird
            self.image = pygame.transform.rotate(self.images[self.index],self.vel * int(-1.5))
       
        else:
             self.image = pygame.transform.rotate(self.images[self.index],-90)   

class Pipe(pygame.sprite.Sprite):
    def __init__(self,x, y, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('img/pipe.png')
        self.rect = self.image.get_rect()
        #position 1 is from the top and position -1 from the bottom
        if position == 1:
            self.image = pygame.transform.flip(self.image, False,True)
            self.rect.bottomleft =[x,y - int(pipe_gap/ 2)]
        if  position == -1:  
          self.rect.topleft =[x,y + int(pipe_gap / 2)]

    def update(self):
        self.rect.x -= move_speed
        if self.rect.right < 0:
            self.kill()



class Button():
     def __init__(self,x,y,image):
         self.image = image
         self.rect = self.image.get_rect()
         self.rect.topleft = (x,y)
    
     def draw(self):

         action = False

         #get mouse position 
         pos = pygame.mouse.get_pos()

         # check if  mouse is  over the button
         if self.rect.collidepoint(pos):
             if pygame.mouse.get_pressed()[0] == 1:
                 action = True

         # draw button
         screen.blit(self.image, (self.rect.x,self.rect.y))

         return action

# bird and pipe parameter
bird_group = pygame.sprite.Group()
pipe_group = pygame.sprite.Group()

# the x and y of the bird and pipe

birdy = Bird(100, int(screen_height / 2))
bird_group.add(birdy)

# restart button intance game
button = Button(screen_width // 2 - 50, screen_height // 2 - 100, button_img)


run = True 
while run:
    
    # fps of the game

    clock.tick(fps)

    # load background and draw bird
    screen.blit(bg,(0,0))
     
    bird_group.draw(screen)
    bird_group.update()

     
    pipe_group.draw(screen)
    
    # the draw the ground
    screen.blit(ground,(ground_move,480))

    # check score
    if len(pipe_group) > 0:
        if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.left\
            and bird_group.sprites()[0].rect.right < pipe_group.sprites()[0].rect.right\
            and pass_pipe == False:
            pass_pipe = True
        if pass_pipe == True:
            if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.right:
                score += 1
                pass_pipe = False
    
  
    draw_text(str(score), font, aoba, int(screen_width / 2), 20)


    #check for collisions
    if pygame.sprite.groupcollide(bird_group,pipe_group, False, False) or birdy.rect.top < 0:
        game_over = True
   
    # check if hit the ground

    if birdy.rect.bottom > 480:
        game_over = True
        flying = False

    if game_over == False and flying == True:

         # generating new pipes
        time_now = pygame.time.get_ticks()
        if time_now - last_pipe > pipe_frequency:
            pipe_height =random.randint(-100,100)
            btm_pipy = Pipe(screen_width, int(screen_height / 2) + pipe_height,-1)
            top_pipy = Pipe(screen_width, int(screen_height / 2 )+ pipe_height,1)
            pipe_group.add(btm_pipy)   # adding to screen 
            pipe_group.add(top_pipy)   # adding to screen 
            last_pipe = time_now
        
           #load ground
        ground_move -= move_speed
        if abs(ground_move) > 35:
            ground_move = 0
        
        pipe_group.update()
        
        # check if game over and restart

    if  game_over == True:
        if button.draw() == True:
          game_over = False
          score = reset_game()
      
    

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run =False
        if event.type == pygame.MOUSEBUTTONDOWN and flying == False and game_over == False:
            flying = True 


    pygame.display.update()

pygame.quit()