# /// script
# dependencies = [
#  "numpy",
# ]
# ///

import numpy
import pygame
from pygame.locals import *
import random
import pygame.sndarray
import json
import asyncio
from fetch import RequestHandler

pygame.init()
fps = 20
score = 0
hs = 0
strikes = 0

mouse_pos = pygame.mouse.get_pos()
sigmaFont = pygame.font.Font('IMG/Others/go3v2.ttf', 50)

def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))
    
def draw_strikes(strikes):
    x_font = pygame.font.Font('IMG/Others/go3v2.ttf', 50)
    red = (255, 0, 0)
    white = (255, 255, 255)
    for i in range(3):
        color = red if i < strikes else white
        scale = 1.5 + i * 0.25
        x_img = x_font.render('X', True, color)
        x_img = pygame.transform.scale(x_img, (int(x_img.get_width() * scale), int(x_img.get_height() * scale)))
        screen.blit(x_img, (screen_width - .000001 + i * 60, 20))

screen_height = 1022
screen_width = 764
bg = pygame.image.load('IMG/Others/Dojo.png')
screen = pygame.display.set_mode((screen_height, screen_width))

normal_fruits = [
    pygame.image.load('IMG/Fruit/Normal_Fruits/fruit_apple_red.png'),
    pygame.image.load('IMG/Fruit/Normal_Fruits/fruit_strawberry.png'),
    pygame.image.load('IMG/Fruit/Normal_Fruits/fruit_watermelon.png'),
    pygame.image.load('IMG/Fruit/Normal_Fruits/fruit_plum.png'),
    pygame.image.load('IMG/Fruit/Normal_Fruits/fruit_apple_green.png'),
    pygame.image.load('IMG/Fruit/Normal_Fruits/fruit_kiwi.png'),
    pygame.image.load('IMG/Fruit/Normal_Fruits/fruit_lime.png'),
    pygame.image.load('IMG/Fruit/Normal_Fruits/fruit_passionfruit.png'),
    pygame.image.load('IMG/Fruit/Normal_Fruits/fruit_banana.png'),
    pygame.image.load('IMG/Fruit/Normal_Fruits/fruit_coconut.png'),
    pygame.image.load('IMG/Fruit/Normal_Fruits/fruit_mango.png'),
    pygame.image.load('IMG/Fruit/Normal_Fruits/fruit_lemon.png'),
    pygame.image.load('IMG/Fruit/Normal_Fruits/fruit_orange.png'),
    pygame.image.load('IMG/Fruit/Normal_Fruits/fruit_pineapple.png'),
    pygame.image.load('IMG/Fruit/Normal_Fruits/fruit_pear (1).png'),
    pygame.image.load('IMG/Fruit/Normal_Fruits/fruit_dragon.png'),
    pygame.image.load('IMG/Fruit/Normal_Fruits/fruit_peach.png'),
]

special_fruits = [
    pygame.image.load('IMG/Fruit/Special_Fruits/Dragon_Fruit.png'),
    pygame.image.load('IMG/Fruit/Special_Fruits/Freeze_Banana.png'),
    pygame.image.load('IMG/Fruit/Special_Fruits/Score_2x_Banana.png'),
    pygame.image.load('IMG/Fruit/Special_Fruits/Starfruit.png'),
    pygame.image.load('IMG/Others/Bomb.png'),
    pygame.image.load('IMG/Others/-10_Bomb.png'),
]

fruit_splatters = [
    pygame.image.load("IMG/Splatters/red_splatter.png"),
    pygame.image.load("IMG/Splatters/green_splatter.png"),
    pygame.image.load("IMG/Splatters/yellow_splatter.png"),
    pygame.image.load("IMG/Splatters/clear_splatter.png"),
]

fruit_slices = [
    pygame.image.load("IMG/Fruit/Fruit_Slices/fruit_apple_red_slice1.png"),
    pygame.image.load("IMG/Fruit/Fruit_Slices/fruit_apple_red_slice2.png"),
    pygame.image.load("IMG/Fruit/Fruit_Slices/fruit_strawberry_slice1.png"),
    pygame.image.load("IMG/Fruit/Fruit_Slices/fruit_strawberry_slice2.png"),
    pygame.image.load("IMG/Fruit/Fruit_Slices/fruit_watermelon_slice1.png"),
    pygame.image.load("IMG/Fruit/Fruit_Slices/fruit_watermelon_slice2.png"),
    pygame.image.load("IMG/Fruit/Fruit_Slices/fruit_plum_slice1.png"),
    pygame.image.load("IMG/Fruit/Fruit_Slices/fruit_plum_slice2.png"),
    pygame.image.load("IMG/Fruit/Fruit_Slices/fruit_apple_green_slice1.png"),
    pygame.image.load("IMG/Fruit/Fruit_Slices/fruit_apple_green_slice2.png"),
    pygame.image.load("IMG/Fruit/Fruit_Slices/fruit_kiwi_slice1.png"),
    pygame.image.load("IMG/Fruit/Fruit_Slices/fruit_kiwi_slice2.png"),
    pygame.image.load("IMG/Fruit/Fruit_Slices/fruit_lime_slice1.png"),
    pygame.image.load("IMG/Fruit/Fruit_Slices/fruit_lime_slice2.png"),
    pygame.image.load("IMG/Fruit/Fruit_Slices/fruit_passionfruit_slice1.png"),
    pygame.image.load("IMG/Fruit/Fruit_Slices/fruit_passionfruit_slice2.png"),
    pygame.image.load("IMG/Fruit/Fruit_Slices/fruit_banana_slice1.png"),
    pygame.image.load("IMG/Fruit/Fruit_Slices/fruit_banana_slice2.png"),
    pygame.image.load("IMG/Fruit/Fruit_Slices/fruit_coconut_slice1.png"),
    pygame.image.load("IMG/Fruit/Fruit_Slices/fruit_coconut_slice2.png"),
    pygame.image.load("IMG/Fruit/Fruit_Slices/fruit_mango_slice1.png"),
    pygame.image.load("IMG/Fruit/Fruit_Slices/fruit_mango_slice2.png"),
    pygame.image.load("IMG/Fruit/Fruit_Slices/fruit_lemon_slice1.png"),
    pygame.image.load("IMG/Fruit/Fruit_Slices/fruit_lemon_slice2.png"),
    pygame.image.load("IMG/Fruit/Fruit_Slices/fruit_orange_slice1.png"),
    pygame.image.load("IMG/Fruit/Fruit_Slices/fruit_orange_slice2.png"),
    pygame.image.load("IMG/Fruit/Fruit_Slices/fruit_pineapple_slice1.png"),
    pygame.image.load("IMG/Fruit/Fruit_Slices/fruit_pineapple_slice2.png"),
    pygame.image.load("IMG/Fruit/Fruit_Slices/fruit_pear_slice1.png"),
    pygame.image.load("IMG/Fruit/Fruit_Slices/fruit_pear_slice2.png"),
    pygame.image.load("IMG/Fruit/Fruit_Slices/fruit_dragon_slice1.png"),
    pygame.image.load("IMG/Fruit/Fruit_Slices/fruit_dragon_slice2.png"),
    pygame.image.load("IMG/Fruit/Fruit_Slices/fruit_peach_slice1.png"),
    pygame.image.load("IMG/Fruit/Fruit_Slices/fruit_peach_slice2.png"),
]

fruit_slice_map = {
    0: (fruit_slices[0], fruit_slices[1]),  # Apple Red
    1: (fruit_slices[2], fruit_slices[3]),  # Strawberry
    2: (fruit_slices[4], fruit_slices[5]),  # Watermelon
    3: (fruit_slices[6], fruit_slices[7]),  # Plum
    4: (fruit_slices[8], fruit_slices[9]),  # Apple Green
    5: (fruit_slices[10], fruit_slices[11]), # Kiwi
    6: (fruit_slices[12], fruit_slices[13]), # Lime
    7: (fruit_slices[14], fruit_slices[15]), # Passionfruit
    8: (fruit_slices[16], fruit_slices[17]), # Banana
    9: (fruit_slices[18], fruit_slices[19]), # Coconut
    10: (fruit_slices[20], fruit_slices[21]),# Mango
    11: (fruit_slices[22], fruit_slices[23]),# Lemon
    12: (fruit_slices[24], fruit_slices[25]),# Orange
    13: (fruit_slices[26], fruit_slices[27]),# Pineapple
    14: (fruit_slices[28], fruit_slices[29]),# Pear
    15: (fruit_slices[30], fruit_slices[31]) # Dragon Fruit
}
#pygame.mixer.Sound("IMG/SFX/fuze.mp3"),
#pygame.mixer.Sound("IMG/SFX/cut1.mp3"),
#pygame.mixer.Sound("IMG/SFX/cut2.mp3"),
#pygame.mixer.Sound("IMG/SFX/metal_pipe.mp3")


for i in range(len(fruit_splatters)):
    fruit_splatters[i] = pygame.transform.scale(fruit_splatters[i], (int(fruit_splatters[i].get_width() * 0.3), int(fruit_splatters[i].get_height() * 0.3)))

poopoopeepee = True
randidx = random.randint(0, 15)
randidxSpecial = random.randint(0, 5)

class Fruit_Normal(pygame.sprite.Sprite):
    global randidx
    def __init__(self, x, y):
        super().__init__()
        self.image = normal_fruits[randidx]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.vel = random.randint(-25, -20)
        self.clicked = False
        self.image.set_alpha(255)
        self.increment = 0

    def splatter_type(self, idx):
        self.idx = idx
        if(idx < 4):
            return 0
        elif(idx < 9):
            return 1
        elif(idx < 16):
            return 2 
        else:
            return 3

    def update(self): 
        if poopoopeepee:  
            mouse_pos = pygame.mouse.get_pos()

        self.vel += 0.5
        self.increment += 1

        self.rect.y += int(self.vel)
        global strikes
        if self.rect.y > 801:
            self.kill()
            strikes += 1
        self.image = pygame.transform.rotate(normal_fruits[randidx], self.vel * -3)

        if self.rect.collidepoint(mouse_pos):
            global score
            global hs
            score += 1
            if score > hs:
                hs = score
            self.kill()
            splatter1 = fruit_slice(self.rect.centerx + random.randint(-10, 10), self.rect.centery, fruit_slice_map[randidx][0])
            splatter2 = fruit_slice(self.rect.centerx + random.randint(-10, 10), self.rect.centery, fruit_slice_map[randidx][1])
            splatter_group.add(splatter1)
            splatter_group.add(splatter2)

class Bomb(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = special_fruits[4]  
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.vel = random.randint(-25, -20)
        self.clicked = False
        self.image.set_alpha(255)
        self.increment = 0

    def update(self): 
        self.vel += 0.5
        self.increment += 1

        self.rect.y += int(self.vel)
        global strikes
        if self.rect.y > 801:
            self.kill()
        self.image = pygame.transform.rotate(special_fruits[4], self.vel * -3)

        if self.rect.collidepoint(pygame.mouse.get_pos()):
            global score
            global hs
            self.kill()
            pygame.quit()

class fruit_slice(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.vel = random.randint(-15, 15)
        self.clicked = False
        self.image.set_alpha(255)

    def update(self): 
        self.vel += 0.5
        self.rect.y += int(self.vel)
        if self.rect.y > 801:
            self.kill()

class Fruit_Special(pygame.sprite.Sprite):
    global randidxSpecial
    
    def __init__(self, x, y):
        super().__init__()
        self.image = special_fruits[randidxSpecial]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.vel = random.randint(-25, -20)
        self.clicked = False
        self.image.set_alpha(255)
        self.increment = 0

    def splatter_type(self, idx):
        self.idx = idx
        if(idx == 0):
            return 0
        elif(idx == 1):
            return 1
        elif(idx == 2):
            return 2 
        elif(idx == 3):
            return 3
        elif(idx == 4):
            return 0

    def update(self): 
        if poopoopeepee:  
            mouse_pos = pygame.mouse.get_pos()

        self.vel += 0.5
        self.increment += 1

        self.rect.y += int(self.vel)
        global strikes 
        if self.rect.y > 801:
            self.kill()
            strikes += 1
        self.image = pygame.transform.rotate(special_fruits[randidxSpecial], self.vel * -3)

        if self.rect.collidepoint(mouse_pos):
            global score
            global hs
            score += 1
            if score > hs:
                hs = score
            self.kill()
            splatter = fruit_splatter(self.rect.centerx, self.rect.centery, self.splatter_type(randidxSpecial))
            splatter_group.add(splatter)

class fruit_splatter(pygame.sprite.Sprite):
    def __init__(self, x, y, fruitType):
        super().__init__()
        self.image = fruit_splatters[fruitType] if fruitType < len(fruit_splatters) else fruit_splatters[0]
        self.rect = self.image.get_rect(center=(x, y))
        self.alpha = 255
        
    def update(self):
        self.alpha = max(0, self.alpha-5)
        self.image.set_alpha(self.alpha)
        if self.alpha <= 0:
            self.kill()

        
trailPos = []

fruit_group = pygame.sprite.Group()
splatter_group = pygame.sprite.Group()

#if random.randint(0,9) == 0:
    #currentSpecialFruit = Fruit_Special(random.randint(0, 700), 800)
   # fruit_group.add(currentSpecialFruit)

#currentFruit = Fruit_Normal(random.randint(0, 700), 800)
#fruit_group.add(currentFruit)

async def main():


    running = True
    while running:

        if len(fruit_group) == 0:
            randidx = random.randint(0, 15)
            currentFruit = Fruit_Normal(random.randint(0, 700), 800)
            fruit_group.add(currentFruit)
            if random.randint(0,2) == 0:
                randidx = random.randint(0, 15)
                currentFruit1 = Fruit_Normal(random.randint(0, 700), 800)
                fruit_group.add(currentFruit1)
            if random.randint(0,5) == 0:
                bomb = Bomb(random.randint(0, 700), 800)
                fruit_group.add(bomb)
        
        balls = False

        font = pygame.font.SysFont('Comic Sans MS', 60)
        white = (255, 255, 255)
        
        screen.blit(bg, (0, 0))
        fruit_group.draw(screen)
        fruit_group.update()
        splatter_group.draw(screen)
        splatter_group.update()

        draw_text("score: "+str(score), sigmaFont, white, int(screen_width/2)-190, 60)
        draw_strikes(strikes)

        mouse_pressed = False

        if strikes > 2:
            running = False
            dataSend = RequestHandler()
            await dataSend.get("http://dreamlo.com/lb/qNZCj8mqsk2JfBWve7H0BAr-L2qGM0jkquvgzgeXgSMA/add/adacar1/"+str(score))
            fakeScoreList = await dataSend.get("http://dreamlo.com/lb/674389178f40bb0e1429f3c6/json")
            scoreList = json.loads(fakeScoreList)
            print(scoreList)
            draw_text('LEADERBOARD', font, white, int(screen_width/2), int(screen_height/2)-300)
            draw_text("1.  "+scoreList['dreamlo']["leaderboard"]['entry'][0]['name'], font, white, int(screen_width/2), int(screen_height/2)-200)
            draw_text(str(scoreList['dreamlo']["leaderboard"]['entry'][0]['score']), font, white, int(screen_width/2) +400, int(screen_height/2)-200)
            draw_text("2.  "+scoreList['dreamlo']["leaderboard"]['entry'][1]['name'], font, white, int(screen_width/2), int(screen_height/2)-100)
            draw_text(str(scoreList['dreamlo']["leaderboard"]['entry'][1]['score']), font, white, int(screen_width/2) +400, int(screen_height/2)-100)            
            draw_text("3.  "+scoreList['dreamlo']["leaderboard"]['entry'][2]['name'], font, white, int(screen_width/2), int(screen_height/2))
            draw_text(str(scoreList['dreamlo']["leaderboard"]['entry'][2]['score']), font, white, int(screen_width/2) +400, int(screen_height/2))
        pygame.display.update()
        await asyncio.sleep(0)
    pygame.quit
asyncio.run(main())




