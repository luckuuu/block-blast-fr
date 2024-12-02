# /// script
# dependencies = [
#  "numpy",
#  "pygame-gui",
#  "python-i18n",
#  "pygame-ce",
# ]
# ///

import numpy
import pygame_gui
import i18n
import pygame
from pygame.locals import *
import random
import sys
import pygame.sndarray
import json
import asyncio
import webbrowser
from fetch import RequestHandler

pygame.init()
pygame.display.set_caption("loading...")

enter = False
name = ""

left_button_img = pygame.transform.scale_by(pygame.image.load("IMG/arrows.png"), 0.1)
right_button_img = pygame.transform.flip(left_button_img, True, False)
down_button_img = pygame.transform.rotate(left_button_img, 90)
rotate_button_img =	pygame.transform.scale_by(pygame.image.load("IMG/rotatebutton.png"), 0.1)




score_rect = pygame.Rect(320, 55, 170, 60)
next_rect = pygame.Rect(320, 215, 170, 180)

screen = pygame.display.set_mode((500, 620))
MANAGER = pygame_gui.UIManager((500, 620))
CLOCK = pygame.time.Clock()
TEXT_INPUT = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((0, 300), (900, 50)), manager=MANAGER, object_id="#main_text_entry")
link_font = pygame.font.SysFont('Consolas', 35)
link_font2 = pygame.font.SysFont('Consolas', 35)
link_font2.set_underline(True)
link_font2.set_italic(True)
link_color = (0, 0, 0)
async def get_user_name():
    global enter
    global name
    screen.fill("white")
    rect = screen.blit(link_font2.render("Click Here if you are on Mobile", True, link_color), (65, 100))
    rect2 = screen.blit(link_font.render("OR type your school username", True, link_color), (65, 200))
    rect3 = screen.blit(link_font.render("(ex. vinpat2) in the box below", True, link_color), (65, 250))
    rect4 = screen.blit(link_font2.render("If on mobile, click here to start", True, link_color), (65, 500))
    while enter == False:
        UI_REFRESH_RATE = CLOCK.tick(60)/1000
        pygame.key.start_text_input()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED and event.ui_object_id == "#main_text_entry":
                enter = True
                name = event.text
                pygame.key.stop_text_input()   
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos

                if rect.collidepoint(pos):
                    webbrowser.open(r"https://docs.google.com/forms/d/e/1FAIpQLScQ-nwkLslAvQTsHIf9P_tSQy_YWWxt20kJp_RNiDeIVCOOPw/viewform?usp=sf_link")
                if rect4.collidepoint(pos):
                    enter = True
                    name = "mobileuser" 
                    pygame.key.stop_text_input()          
            
            MANAGER.process_events(event)
            await asyncio.sleep(0)

        MANAGER.update(UI_REFRESH_RATE)

        MANAGER.draw_ui(screen)

        pygame.display.update()
        await asyncio.sleep(0)

clock = pygame.time.Clock()


GAME_UPDATE = pygame.USEREVENT
pygame.time.set_timer(GAME_UPDATE, 200)

def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

class Block:
    def __init__(self, id):
        self.id = id
        self.cells = {}
        self.cell_size = 30
        self.row_offset = 0
        self.column_offset = 0
        self.rotation_state = 0
        self.colors = Colors.get_cell_colors()

    def move(self, rows, columns):
        self.row_offset += rows
        self.column_offset += columns

    def get_cell_positions(self):
        tiles = self.cells[self.rotation_state]
        moved_tiles = []
        for position in tiles:
            position = Position(position.row + self.row_offset, position.column + self.column_offset)
            moved_tiles.append(position)
        return moved_tiles

    def rotate(self):
        self.rotation_state += 1
        if self.rotation_state == len(self.cells):
            self.rotation_state = 0

    def undo_rotation(self):
        self.rotation_state -= 1
        if self.rotation_state == -1:
            self.rotation_state = len(self.cells) - 1

    def draw(self, screen, offset_x, offset_y):
        tiles = self.get_cell_positions()
        for tile in tiles:
            tile_rect = pygame.Rect(offset_x + tile.column * self.cell_size, 
                offset_y + tile.row * self.cell_size, self.cell_size -1, self.cell_size -1)
            pygame.draw.rect(screen, self.colors[self.id], tile_rect)

class LBlock(Block):
    def __init__(self):
        super().__init__(id = 1)
        self.cells = {
            0: [Position(0, 2), Position(1, 0), Position(1, 1), Position(1, 2)],
            1: [Position(0, 1), Position(1, 1), Position(2, 1), Position(2, 2)],
            2: [Position(1, 0), Position(1, 1), Position(1, 2), Position(2, 0)],
            3: [Position(0, 0), Position(0, 1), Position(1, 1), Position(2, 1)]
        }
        self.move(0, 3)

class JBlock(Block):
    def __init__(self):
        super().__init__(id = 2)
        self.cells = {
            0: [Position(0, 0), Position(1, 0), Position(1, 1), Position(1, 2)],
            1: [Position(0, 1), Position(0, 2), Position(1, 1), Position(2, 1)],
            2: [Position(1, 0), Position(1, 1), Position(1, 2), Position(2, 2)],
            3: [Position(0, 1), Position(1, 1), Position(2, 0), Position(2, 1)]
        }
        self.move(0, 3)

class IBlock(Block):
    def __init__(self):
        super().__init__(id = 3)
        self.cells = {
            0: [Position(1, 0), Position(1, 1), Position(1, 2), Position(1, 3)],
            1: [Position(0, 2), Position(1, 2), Position(2, 2), Position(3, 2)],
            2: [Position(2, 0), Position(2, 1), Position(2, 2), Position(2, 3)],
            3: [Position(0, 1), Position(1, 1), Position(2, 1), Position(3, 1)]
        }
        self.move(-1, 3)

class OBlock(Block):
    def __init__(self):
        super().__init__(id = 4)
        self.cells = {
            0: [Position(0, 0), Position(0, 1), Position(1, 0), Position(1, 1)]
        }
        self.move(0, 4)

class SBlock(Block):
    def __init__(self):
        super().__init__(id = 5)
        self.cells = {
            0: [Position(0, 1), Position(0, 2), Position(1, 0), Position(1, 1)],
            1: [Position(0, 1), Position(1, 1), Position(1, 2), Position(2, 2)],
            2: [Position(1, 1), Position(1, 2), Position(2, 0), Position(2, 1)],
            3: [Position(0, 0), Position(1, 0), Position(1, 1), Position(2, 1)]
        }
        self.move(0, 3)

class TBlock(Block):
    def __init__(self):
        super().__init__(id = 6)
        self.cells = {
            0: [Position(0, 1), Position(1, 0), Position(1, 1), Position(1, 2)],
            1: [Position(0, 1), Position(1, 1), Position(1, 2), Position(2, 1)],
            2: [Position(1, 0), Position(1, 1), Position(1, 2), Position(2, 1)],
            3: [Position(0, 1), Position(1, 0), Position(1, 1), Position(2, 1)]
        }
        self.move(0, 3)

class ZBlock(Block):
    def __init__(self):
        super().__init__(id = 7)
        self.cells = {
            0: [Position(0, 0), Position(0, 1), Position(1, 1), Position(1, 2)],
            1: [Position(0, 2), Position(1, 1), Position(1, 2), Position(2, 1)],
            2: [Position(1, 0), Position(1, 1), Position(2, 1), Position(2, 2)],
            3: [Position(0, 1), Position(1, 0), Position(1, 1), Position(2, 0)]
        }
        self.move(0, 3)

class Game:
    def __init__(self):
        self.grid = Grid()
        self.blocks = [IBlock(), JBlock(), LBlock(), OBlock(), SBlock(), TBlock(), ZBlock()]
        self.current_block = self.get_random_block()
        self.next_block = self.get_random_block()
        self.game_over = False
        self.score = 0

    def update_score(self, lines_cleared, move_down_points):
        if lines_cleared == 1:
            self.score += 100
        elif lines_cleared == 2:
            self.score += 300
        elif lines_cleared == 3:
            self.score += 500
        elif lines_cleared == 4:
            self.score += 1000
        self.score += move_down_points

    def get_random_block(self):
        if len(self.blocks) == 0:
            self.blocks = [IBlock(), JBlock(), LBlock(), OBlock(), SBlock(), TBlock(), ZBlock()]
        block = random.choice(self.blocks)
        self.blocks.remove(block)
        return block

    def move_left(self):
        self.current_block.move(0, -1)
        if self.block_inside() == False or self.block_fits() == False:
            self.current_block.move(0, 1)

    def move_right(self):
        self.current_block.move(0, 1)
        if self.block_inside() == False or self.block_fits() == False:
            self.current_block.move(0, -1)

    def move_down(self):
        self.current_block.move(1, 0)
        if self.block_inside() == False or self.block_fits() == False:
            self.current_block.move(-1, 0)
            self.lock_block()

    def lock_block(self):
        tiles = self.current_block.get_cell_positions()
        for position in tiles:
            self.grid.grid[position.row][position.column] = self.current_block.id
        self.current_block = self.next_block
        self.next_block = self.get_random_block()
        rows_cleared = self.grid.clear_full_rows()
        if rows_cleared > 0:
            self.update_score(rows_cleared, 0)
        if self.block_fits() == False:
            self.game_over = True

    def reset(self):
        self.grid.reset()
        self.blocks = [IBlock(), JBlock(), LBlock(), OBlock(), SBlock(), TBlock(), ZBlock()]
        self.current_block = self.get_random_block()
        self.next_block = self.get_random_block()
        self.score = 0

    def block_fits(self):
        tiles = self.current_block.get_cell_positions()
        for tile in tiles:
            if self.grid.is_empty(tile.row, tile.column) == False:
                return False
        return True

    def rotate(self):
        self.current_block.rotate()
        if self.block_inside() == False or self.block_fits() == False:
            self.current_block.undo_rotation()

    def block_inside(self):
        tiles = self.current_block.get_cell_positions()
        for tile in tiles:
            if self.grid.is_inside(tile.row, tile.column) == False:
                return False
        return True

    def draw(self, screen):
        self.grid.draw(screen)
        self.current_block.draw(screen, 11, 11)

        if self.next_block.id == 3:
            self.next_block.draw(screen, 255, 290)
        elif self.next_block.id == 4:
            self.next_block.draw(screen, 255, 280)
        else:
            self.next_block.draw(screen, 270, 270)

class Grid:
    def __init__(self):
        self.num_rows = 20
        self.num_cols = 10
        self.cell_size = 30
        self.grid = [[0 for j in range(self.num_cols)] for i in range(self.num_rows)]
        self.colors = Colors.get_cell_colors()

    def print_grid(self):
        for row in range(self.num_rows):
            for column in range(self.num_cols):
                print(self.grid[row][column], end = " ")
            print()

    def is_inside(self, row, column):
        if row >= 0 and row < self.num_rows and column >= 0 and column < self.num_cols:
            return True
        return False

    def is_empty(self, row, column):
        if self.grid[row][column] == 0:
            return True
        return False

    def is_row_full(self, row):
        for column in range(self.num_cols):
            if self.grid[row][column] == 0:
                return False
        return True

    def clear_row(self, row):
        for column in range(self.num_cols):
            self.grid[row][column] = 0

    def move_row_down(self, row, num_rows):
        for column in range(self.num_cols):
            self.grid[row+num_rows][column] = self.grid[row][column]
            self.grid[row][column] = 0

    def clear_full_rows(self):
        completed = 0
        for row in range(self.num_rows-1, 0, -1):
            if self.is_row_full(row):
                self.clear_row(row)
                completed += 1
            elif completed > 0:
                self.move_row_down(row, completed)
        return completed

    def reset(self):
        for row in range(self.num_rows):
            for column in range(self.num_cols):
                self.grid[row][column] = 0

    def draw(self, screen):
        for row in range(self.num_rows):
            for column in range(self.num_cols):
                cell_value = self.grid[row][column]
                cell_rect = pygame.Rect(column*self.cell_size + 11, row*self.cell_size + 11,
                self.cell_size -1, self.cell_size -1)
                pygame.draw.rect(screen, self.colors[cell_value], cell_rect)

class Position:
    def __init__(self, row, column):
        self.row = row
        self.column = column


class Colors:
    dark_grey = (26, 31, 40)
    green = (47, 230, 23)
    red = (232, 18, 18)
    orange = (226, 116, 17)
    yellow = (237, 234, 4)
    purple = (166, 0, 247)
    cyan = (21, 204, 209)
    blue = (13, 64, 216)
    white = (255, 255, 255)
    dark_blue = (44, 44, 127)
    light_blue = (59, 85, 162)

    @classmethod
    def get_cell_colors(cls):
        return [cls.dark_grey, cls.green, cls.red, cls.orange, cls.yellow, cls.purple, cls.cyan, cls.blue]


class Button:
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
    
    def draw(self):

        self.action = False

        #get mouse pos
        m_pos = pygame.mouse.get_pos()

        #check if mouse in on button
        if self.rect.collidepoint(m_pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                self.action = True
                
            if pygame.mouse.get_pressed()[0] == 0:
                self.action = False
                self.clicked = False

        #draw button
        screen.blit(self.image, (self.rect.x, self.rect.y))

        return self.action



title_font = pygame.font.Font(None, 40)
score_surface = title_font.render("Score", True, Colors.white)
next_surface = title_font.render("Next", True, Colors.white)
game_over_surface = title_font.render("GAME OVER", True, Colors.white)

left_button = Button(340, 450, left_button_img)
right_button = Button(410, 450, right_button_img)
down_button = Button(375, 500, down_button_img)
rotate_button = Button(375, 400, rotate_button_img)

game = Game()
font = pygame.font.SysFont('Comic Sans MS', 40)
white = (255, 255, 255)

asyncio.run(get_user_name())

async def main():

    running = True
    while running:

        if enter:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if (event.key == pygame.K_LEFT or left_button.draw()) and game.game_over == False:
                        game.move_left()
                    if (event.key == pygame.K_RIGHT or right_button.draw()) and game.game_over == False:
                        game.move_right()
                    if (event.key == pygame.K_DOWN or down_button.draw()) and game.game_over == False:
                        game.move_down()
                        game.update_score(0, 1)
                    if (event.key == pygame.K_UP or rotate_button.draw()) and game.game_over == False:
                        game.rotate()
                if event.type == GAME_UPDATE and game.game_over == False:
                    game.move_down()

            #Drawing
            score_value_surface = title_font.render(str(game.score), True, Colors.white)
            draw_text(str(name), font, white, 365, 120)
            

            screen.fill(Colors.dark_blue)
            screen.blit(score_surface, (365, 20, 50, 50))
            screen.blit(next_surface, (375, 180, 50, 50))

            pygame.draw.rect(screen, Colors.light_blue, score_rect, 0, 10)
            screen.blit(score_value_surface, score_value_surface.get_rect(centerx = score_rect.centerx, 
                centery = score_rect.centery))
            pygame.draw.rect(screen, Colors.light_blue, next_rect, 0, 10)
            game.draw(screen)

            if left_button.draw():
                game.move_left()

            if right_button.draw():
                game.move_right()

            if down_button.draw():
                game.move_down()
                game.update_score(0, 1)

            if rotate_button.draw():
                game.rotate()
            
            if game.game_over == True:
                running = False
                screen.blit(game_over_surface, (320, 450, 50, 50))
                dataSend = RequestHandler()
                await dataSend.get("https://dreamlo.com/lb/qNZCj8mqsk2JfBWve7H0BAr-L2qGM0jkquvgzgeXgSMA/add/"+str(name)+"/"+str(game.score))
                fakeScoreList = await dataSend.get("https://dreamlo.com/lb/674389178f40bb0e1429f3c6/json")
                scoreList = json.loads(fakeScoreList)
                draw_text('LEADERBOARD', font, white, 50, int(620/2)-200)
                draw_text("1.  "+scoreList['dreamlo']["leaderboard"]['entry'][0]['name'] + ":", font, white, 50, int(620/2)-100)
                draw_text(str(scoreList['dreamlo']["leaderboard"]['entry'][0]['score']), font, white, 50 +200, int(620/2)-100)
                draw_text("2.  "+scoreList['dreamlo']["leaderboard"]['entry'][1]['name'] + ":", font, white, 50, int(620/2))
                draw_text(str(scoreList['dreamlo']["leaderboard"]['entry'][1]['score']), font, white, 50 +200, int(620/2))            
                draw_text("3.  "+scoreList['dreamlo']["leaderboard"]['entry'][2]['name'] + ":", font, white, 50, int(620/2)+100)
                draw_text(str(scoreList['dreamlo']["leaderboard"]['entry'][2]['score']), font, white, 50 +200, int(620/2)+100)
            pygame.display.update()
            clock.tick(60)
        await asyncio.sleep(0)
    pygame.quit
asyncio.run(main())