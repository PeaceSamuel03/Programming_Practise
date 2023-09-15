#PYGAME PLATFORMER TYPE GAME
"""IMPORT PACKAGES/MODULES"""
import pygame
from pygame.locals import *
from pygame.sprite import *


pygame.init() #initialize pygame
#frame rate for game/ allows game to run at same rate regardless of device
clock = pygame.time.Clock()
fps = 60
#create game screen
size = width, height = 1000, 800
screen = pygame.display.set_mode(size)
pygame.display.set_caption("PY_PLATFORMER")

#GAME VARIABLES
tile_size = 50 #50 pixels for tile size, ie. screen 20*16 grid
game_over = 0
main_menu = True
level = 1

#LOAD IMAGES
bg_img = pygame.image.load('bg.jpg')
bg_img = pygame.transform.scale(bg_img,(width,height))
restart_img = pygame.image.load('restart_button.png')
restart_img = pygame.transform.scale(restart_img,(150,50))
start_img = pygame.image.load('start_button.png')
start_img = pygame.transform.scale(start_img, (150, 50))
exit_img = pygame.image.load('exit_button.png')
exit_img = pygame.transform.scale(exit_img, (150, 50))


class Button():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.clicked = False

    def draw(self):
        action = False
        #get mouse position
        pos = pygame.mouse.get_pos()

        #check mouseover and click conditions
        if self.rect.collidepoint(pos):
            #check for click, left mouse click is at index 0
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                action = True
                self.clicked = True
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        #draw button to screen
        screen.blit(self.image, self.rect)
        return action

class Player():
    def __init__(self, x, y):
        self.reset(x, y)#used to create initial points for player

    def update(self, game_over):
        """steps: find player position -> check for collision-> move player position"""
        """add player movement/ animation"""
        #values for player position change/ movement
        dx = 0
        dy = 0
        walk_cooldown = 5

        if game_over == 0:
            #get key presses, for player movement
            key = pygame.key.get_pressed()
            #jump, with gravity, can only jump once (jump if not already in air)
            if key[pygame.K_SPACE] and self.jumped == False and self.in_air == False:
                self.vel_y = -15
                self.jumped = True
            if key[pygame.K_SPACE] == False:
                #when space key is released
                self.jumped = False

            #add gravity
            self.vel_y += 1
            if self.vel_y > 10:
                self.vel_y = 10
            dy += self.vel_y

            #move left & right
            if key[pygame.K_LEFT]:
                dx -= 5
                self.counter += 1
                self.direction = -1
            if key[pygame.K_RIGHT]:
                dx += 5
                self.counter += 1
                self.direction = 1
            #animation stops if keys not pressed
            if key[pygame.K_LEFT] == False and key[pygame.K_RIGHT] == False:
                self.counter = 0
                self.index = 0
                if self.direction == 1:
                    self.image = self.images_right[self.index]
                if self.direction == -1:
                    self.image = self.images_left[self.index]

            #handle animation
            if self.counter > walk_cooldown:
                self.counter = 0 #counter increases when arrow keys are pressed
                self.index += 1#increase index
                #prevent index from going over the len of the list
                if self.index >= len(self.images_right):
                    self.index = 0
                #check direction 
                if self.direction == 1:
                    self.image = self.images_right[self.index]
                if self.direction == -1:
                    self.image = self.images_left[self.index]

            #check for collision
            self.in_air = True
            for tile in world.tile_list:
                #check for collision in x direction
                if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                    dx = 0
                #check for collision in y direction
                if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                    #check if below ground ie. jumping and hit head on block
                    if self.vel_y < 0:
                        dy = tile[1].bottom - self.rect.top
                        self.vel_y = 0
                    #check if above ground ie. falling
                    elif self.vel_y >= 0:
                        dy = tile[1].top - self.rect.bottom
                        self.vel_y = 0
                        self.in_air = False #has landed onto something

            #check for collision with enemies
            if pygame.sprite.spritecollide(self, ghost_group, False):
                game_over = -1 #-1 -> player has died
            
            #check for collision with lava
            if pygame.sprite.spritecollide(self, lava_group, False):
                game_over = -1

            #check collision with exit door
            if pygame.sprite.spritecollide(self, exit_group, False):
                game_over = 1 #1 -> player has won
                
            #update player position
            self.rect.x += dx
            self.rect.y += dy

        elif game_over == -1:
            self.image = self.dead_image
            self.image = pygame.transform.scale(self.dead_image, (40,50))
            if self.rect.y > 50:
                self.rect.y -= 5 

        #draw player unto screen
        screen.blit(self.image, self.rect)

        return game_over
    
    def reset(self, x, y):
            self.images_right = []#images used to animate movement to the right
            self.images_left = []#images used to animate left
            self.index = 0#corresponds to images in list
            self.counter = 0 #speed at which images are changed for animation
            for num in range(1,6):
                #load images, each num corresponds to image
                img_right = pygame.image.load(f'player{num}.png')
                img_right = pygame.transform.scale(img_right, (40,80))
                img_left = pygame.transform.flip(img_right, True, False)#true for x axis flip
                self.images_right.append(img_right)#append images to list
                self.images_left.append(img_left)
            self.dead_image = pygame.image.load('death1.png')
            self.image = self.images_right[self.index]
            self.rect = self.image.get_rect()# create rect object
            self.rect.x = x
            self.rect.y = y
            self.width = self.image.get_width()
            self.height = self.image.get_height()
            self.vel_y = 0 #velocity in the y direction, for gradual jump
            self.jumped = False #can't hold the space bar for a long jump
            self.direction = 0
            self.in_air = True

class World():
    def __init__(self, data:list):
        """used to draw tiles onto the screen in the given pattern"""
        self.tile_list = []

        #load images
        dirt_img = pygame.image.load('dirt.png')#Assigned number -> 1
        grass_img = pygame.image.load('grass.png')#Assign -> 2
        #Draw a dirt and grass around the 'World'/screen
        #use grid pattern of the world screen, 20*16 tiles, each of 50 pixels
        
        row_count = 0
        for row in data:
            col_count = 0
            for tile in row:
                if tile == 1:
                    #scale img to tile size
                    img = pygame.transform.scale(dirt_img,(tile_size,tile_size))
                    img_rect = img.get_rect()#make rect object
                    #move x and y position according to tile size
                    #each tile position is dependant on its row and column
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)#store tile data
                    self.tile_list.append(tile)
                if tile == 2:
                    #scale img to tile size
                    img = pygame.transform.scale(grass_img,(tile_size,tile_size))
                    img_rect = img.get_rect()#make rect object
                    #move x and y position according to tile size
                    #each tile position is dependant on its row and column
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)#store tile data
                    self.tile_list.append(tile)
                if tile == 3:
                    ghost = Enemy(col_count * tile_size, row_count* tile_size)
                    ghost_group.add(ghost) #add new ghost to sprite group
                if tile == 4:
                    lava = Lava(col_count * tile_size, row_count* tile_size + (tile_size // 2))
                    lava_group.add(lava)
                if tile == 5:
                    exit = Exit(col_count * tile_size, row_count * tile_size - (tile_size // 2))
                    exit_group.add(exit)
                col_count += 1
            row_count += 1
        
    def draw(self):
        for tile in self.tile_list:
            #data needed to draw is stored in the list
            #tile data stored as image in index 0  and rect data in index 1 of tuple
            screen.blit(tile[0], tile[1])

class Enemy(pygame.sprite.Sprite):
    #Sprites in pygame are a tool used to manage and manipulate graphical elements within a game.
    #Used to represent characters, objects, visual effects etc. that need to be displayed on the screen.
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self) #call to inherit from super class
        image = pygame.image.load('ghost.png')#need to find enemy image
        self.image = pygame.transform.scale(image,(tile_size,tile_size))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.move_direction = 1
        self.move_counter = 0

    def update(self):
        self.rect.x += self.move_direction #move to the right
        self.move_counter += 1
        if abs(self.move_counter) > 50:
            self.move_direction *= -1 #change direction
            self.move_counter *= -1 #flip counter, opposite direction

class Lava(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self) #call to inherit from super class
        image = pygame.image.load('lava.png')#need to find enemy image
        self.image = pygame.transform.scale(image,(tile_size,tile_size))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
class Exit(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self) #call to inherit from super class
        image = pygame.image.load('exit.png')#need to find enemy image
        self.image = pygame.transform.scale(image,(tile_size,int(tile_size * 1.5)))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y 


world_data = [
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 1],
[1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 3, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 1],
[1, 0, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 2, 0, 2, 2, 2, 2, 2, 1],
[1, 0, 0, 0, 0, 0, 2, 2, 2, 4, 4, 4, 4, 4, 1, 1, 1, 1, 1, 1],
[1, 0, 0, 0, 0, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
[1, 0, 0, 0, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
[1, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

#CREATE CLASS INSTANCES
ghost_group = pygame.sprite.Group()
lava_group = pygame.sprite.Group()
exit_group = pygame.sprite.Group()
player = Player(100, height - 130)
 
world = World(world_data)

#create buttons
restart_button = Button((width //2) -50, height //2, restart_img)
start_button = Button((width // 2)-200, (height //2), start_img)
exit_button = Button((width // 2), (height //2), exit_img)


running = True
while running:
    clock.tick(fps)#set frame rate
    #draw onto screen
    screen.blit(bg_img, (0,0))
    if main_menu == True:
        if exit_button.draw(): #returns if clicked or not
            running = False
        if start_button.draw(): #clicked
            main_menu = False
    else:
        world.draw() 
        #stop enemy movement when game is over
        if game_over == 0:
            ghost_group.update()
        ghost_group.draw(screen)
        lava_group.draw(screen)
        exit_group.draw(screen)
        game_over = player.update(game_over) #get the returned game_over variable

        if game_over == -1: #player has died
            if restart_button.draw(): #returns True or False
                player.reset(100, height - 130) #reset player
                game_over = 0 #no longer game over condition
        
        if game_over == 1: #player has won/ completed game level
            color = (255, 0, 200)
            bg_color = (255, 255, 255)
            font = pygame.font.Font("freesansbold.ttf", 32)
            text = font.render("You have won!!", True, color, bg_color)
            text_rect = text.get_rect()
            text_rect.center = (width //2, height //2)
            screen.blit(text, text_rect)



    #EVENT HANDLER
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.update()
pygame.quit()