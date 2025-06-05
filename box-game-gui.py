import pygame
import sys
import random

debug_mode = False

# -------- INTERFACE ------------
# Constants
## GUI
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 1280*9//16

## BOXES
BOX_WIDTH = 90
BOX_HEIGHT = 130
BOX_DX = 15
BOX_MEDIUM_HEIGHT = int(0.3*WINDOW_HEIGHT)
BOX_DOOR_OFFSET = 0.5
BOX_HOLE_Y = BOX_MEDIUM_HEIGHT - BOX_HEIGHT//2
BOX_DOOR_Y = BOX_HOLE_Y - int(BOX_HEIGHT*BOX_DOOR_OFFSET)
DOOR_EDGE_RATIO = 0.1
DOOR_EDGE_HEIGHT = int(DOOR_EDGE_RATIO*BOX_HEIGHT)
DOOR_EDGE_Y = BOX_DOOR_Y + BOX_HEIGHT - DOOR_EDGE_HEIGHT
HITBOX_HEIGHT = BOX_HEIGHT*(1+BOX_DOOR_OFFSET)
FONT_SIZE_NUMBER = 84

## Message
FONT_SIZE_MESSAGE = 54
INITIAL_TEXT = 'Clique "Rolar" para começar!'
MESSAGE_X = 180
MESSAGE_Y = 660

## Buttons
BUTTON_WIDTH = 300
BUTTON_HEIGHT = 70

### GAME
BUTTON_X = 800
ROLL_BUTTON_Y = 500
BUTTON_DY = 20
RESET_BUTTON_Y = ROLL_BUTTON_Y+BUTTON_DY+BUTTON_HEIGHT
RETURN_BUTTON_Y = RESET_BUTTON_Y+BUTTON_DY+BUTTON_HEIGHT
FONT_SIZE_BUTTON = 54

### MENU
MENU_BUTTON_X = (WINDOW_WIDTH - BUTTON_WIDTH)//2

## Dice
DIE_SIZE = 64
SCALED_DIE_SIZE = DIE_SIZE*3
DIE_Y = 350
DIE_X = 180
DIE_DX = 30

ANIMATION_TIME = 1300 # ms
FRAME_DURATION = 50 # ms

# Colors
BACKGROUND_COLOR = pygame.Color(220,180,150)
HOLE_COLOR = pygame.Color(100,50,0)
DOOR_COLOR = pygame.Color(220,120,30)
DOOR_EDGE_COLOR = pygame.Color(180,80,10)
NUMBER_COLOR = pygame.Color(248, 242, 223)
MESSAGE_COLOR = pygame.Color(15,15,60)
ROLL_BACK_COLOR = pygame.Color(190,30,40)
ROLL_TEXT_COLOR = pygame.Color(248, 242, 223)
RESET_BACK_COLOR = pygame.Color(248, 242, 223)
RESET_TEXT_COLOR = MESSAGE_COLOR


def set_boxes(number):
    return [Box(i,number) for i in range(1,number+1)]

def display_message(string):
    font = pygame.font.SysFont(None, FONT_SIZE_MESSAGE)
    text_surface = font.render(message, True, MESSAGE_COLOR)  # black text
    text_rect = text_surface.get_rect(bottomleft=(MESSAGE_X,MESSAGE_Y))
    WINDOW.blit(text_surface, text_rect)


class Box(object):
    def __init__(self, value, total_number):
        self.value = value
        self.num_boxes = total_number
        self.set_rects()
        self.is_clickable = True
        self.is_shut = False

        self.door_altered = 0
        self.win_state = 0 # -1 = perda, 1 = vitória

    def set_rects(self):
        box_row_width = BOX_WIDTH*self.num_boxes + BOX_DX*(self.num_boxes-1)
        origin_x = WINDOW_WIDTH//2 - box_row_width//2
        dx = (BOX_DX+BOX_WIDTH)*(self.value-1)
        this_x = origin_x+dx

        self.hole = pygame.Rect(this_x, BOX_HOLE_Y, BOX_WIDTH, BOX_HEIGHT)
        self.door = pygame.Rect(this_x, BOX_DOOR_Y, BOX_WIDTH, BOX_HEIGHT)
        self.door_edge = pygame.Rect(this_x, DOOR_EDGE_Y, BOX_WIDTH, DOOR_EDGE_HEIGHT)

        self.hitbox = pygame.Rect(this_x, BOX_DOOR_Y, BOX_WIDTH, HITBOX_HEIGHT)

    def process_click(self):
        if not self.is_clickable:
            return 0
        
        signal = (-1)**self.is_shut
        self.door.top += int(signal*BOX_HEIGHT*BOX_DOOR_OFFSET)
        self.door_edge.top += int(signal*BOX_HEIGHT*BOX_DOOR_OFFSET)
        self.hitbox.top += int(signal*BOX_HEIGHT*BOX_DOOR_OFFSET)
        self.hitbox.height -= int(signal*BOX_HEIGHT*BOX_DOOR_OFFSET)

        self.is_shut = not self.is_shut
        return signal*self.value
    
    def reset(self):
        self.set_rects()

        self.is_clickable = False
        self.is_shut = False

    def draw(self):
        # Rects
        pygame.draw.rect(WINDOW, HOLE_COLOR, self.hole)
        pygame.draw.rect(WINDOW, DOOR_COLOR, self.door)
        pygame.draw.rect(WINDOW, DOOR_EDGE_COLOR, self.door_edge)

        # Value
        font = pygame.font.SysFont(None, FONT_SIZE_NUMBER)
        text_surface = font.render(str(self.value), True, NUMBER_COLOR)  # black text
        text_rect = text_surface.get_rect(center=self.door.center)
        WINDOW.blit(text_surface, text_rect)

class Message(object):
    def __init__(self, default, size, color=MESSAGE_COLOR, **kwargs):
        self.text = default
        self.font = pygame.font.SysFont(None, size)
        self.surface = self.font.render(self.text, True, color)
        self.color = color
        
        if 'bottomleft' in kwargs:
            self.rect = self.surface.get_rect(bottomleft=kwargs['bottomleft'])
        elif 'topleft' in kwargs:
            self.rect = self.surface.get_rect(bottomleft=kwargs['topleft'])
        else:
            raise TypeError('Informa a posição do retângulo ô gayzinho')

    def display(self):
        WINDOW.blit(self.surface,self.rect)

    def set_text(self, text):
        self.text = text
        self.surface = self.font.render(self.text, True, self.color)

class Button(object):
    def __init__(self, label, x, y, color, text_color, effect):
        self.rect = pygame.Rect(x,y,BUTTON_WIDTH,BUTTON_HEIGHT)
        self.process_click = effect
        self.color = color

        font = pygame.font.SysFont(None, FONT_SIZE_BUTTON)
        self.text_surface = font.render(label, True, text_color)
        self.text_rect = self.text_surface.get_rect(center=self.rect.center)
    def draw(self):
        pygame.draw.rect(WINDOW, self.color, self.rect)
        WINDOW.blit(self.text_surface, self.text_rect)        

class Die(object):
    def __init__(self, x, y):
        self.spritesheet = pygame.image.load('./dice-spritesheet.png')
        self.value = 6
        self.topleft = (x,y)

    def draw(self):
        x = DIE_SIZE*(self.value-1)
        rect = pygame.Rect(x,0,DIE_SIZE,DIE_SIZE)
        sprite = self.spritesheet.subsurface(rect).copy()
        sprite = pygame.transform.scale(sprite, (SCALED_DIE_SIZE,SCALED_DIE_SIZE))

        WINDOW.blit(sprite,self.topleft)

# -------- LOGIC ------------
class Game(object):
    def __init__(self, door_count=9):
        self.boxes = set_boxes(door_count)
        self.doors = {i:False for i in range(1,door_count+1)} # True = fechada
        self.score_to_reach = 0

        die1 = Die(DIE_X, DIE_Y)
        die2 = Die(DIE_X+SCALED_DIE_SIZE+DIE_DX, DIE_Y)
        self.dice = [die1, die2]

        self.is_rolling = False
        self.is_closing = False
        self.should_reset = False
        self.game_over = False

        self.last_value = 0
        self.current_sum = 0

        self.game_screen = 0
        # 0: Menu
        # 1: Rules
        # 2: Game


    def get_box(self,value):
        return self.boxes[value-1]

    # CHANGE    
    def roll_die(self):
        return random.randint(1,6)
    
    def roll_dice(self, buttons, message):
        # Tempo de animação
        starting_time = pygame.time.get_ticks()
        while True:
            now = pygame.time.get_ticks()
            elapsed = now - starting_time

            if elapsed >= ANIMATION_TIME:
                break
            else:
                [die1, die2] = self.dice
                die1.value = self.roll_die()
                die2.value = self.roll_die()
                first_frame = pygame.time.get_ticks()
                while True:
                    frame_now = pygame.time.get_ticks()
                    frame_elapsed = frame_now - first_frame

                    if frame_elapsed >= FRAME_DURATION:
                        break
                    
                    self.render(buttons, message)

        roll1 = self.roll_die()
        roll2 = self.roll_die()

        if debug_mode:
            return 3, 6

        return roll1, roll2

    def get_open(self):
        return [i for i in self.doors if not self.doors[i]]
    
    def close_door(self, index):
        doors = self.doors

        if doors[index]:
            return False
        
        doors[index] = True
        return True
        
    def get_possibilities(self):
        points = self.score_to_reach
        possibilities = []
        available_doors = [i for i in self.doors if not self.doors[i] and i <= points]

        while len(available_doors) > 0:
            node = available_doors.pop() # Pega o maior nó como inicial
            frontier = []
            thread = [node]
            cost = node
            father = None

            while True:
                
                # Se atingiu a soma, essa é uma possibilidade
                if cost == points:
                    possibilities.append(list(thread))
                    thread.pop() # Remove último elemento da thread
                    if len(thread) == 0: # Se era uma thread unitária, acabou a exploração
                        break
                
                # Se não atingiu a soma, segue explorando
                # Obtém a fronteira do nodo atual
                # Está na fronteira todo nodo menor que não ultrapasse o total de pontos
                else:
                    frontier = frontier + [(node, i) for i in available_doors if i<node and cost+i <= points]

                if len(frontier) == 0:
                    break

                father, next = frontier.pop()
                while thread[-1] != father:
                    thread.pop()
                node = next
                thread.append(node)
                cost = sum(thread)
        return possibilities                 

    def game_loop(self, message, buttons):
        self.handle_inputs(buttons)

        if self.should_reset:
            self.should_reset = False
            self.reset(message)

        elif self.game_over != 0:
            if self.game_over == -1:
                message.set_text("Você perdeu, perdedor >:(")
                for box in self.boxes:
                    box.is_clickable = False

            else:
                message.set_text("Você ganhou! Que lacre")

        elif self.is_rolling:
            rolls = self.roll_dice(buttons, message)
            [die1, die2] = self.dice
            die1.value = rolls[0]
            die2.value = rolls[1]
            self.score_to_reach = sum(rolls)
            text = f'Feche portas somando {self.score_to_reach}'
            message.set_text (text)
            self.is_rolling = False
            self.is_closing = True
            self.current_sum = 0
            for box in self.boxes:
                box.is_clickable = not box.is_shut

            self.possibilities = self.get_possibilities()
            #print(self.possibilities)

        

        # Process input
        if self.is_closing:

            if len(self.possibilities) == 0:
                self.game_over = -1

            elif self.current_sum == self.score_to_reach:
                self.is_closing = False
                for box in self.boxes:
                    box.is_clickable = False
                    if box.is_shut:
                        self.doors[box.value] = True

                if all(box.is_shut for box in self.boxes):
                    self.game_over = 1


            elif self.last_value != 0:
                self.current_sum += self.last_value
                self.last_value = 0
                #print(self.current_sum)
        

        self.render(buttons,message)
    
    def handle_inputs(self, buttons):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or \
            event.type == pygame.KEYDOWN and event.key == event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                for box in self.boxes:
                    if box.hitbox.collidepoint(event.pos):
                        self.last_value = box.process_click()

                for button in buttons:
                    if button.rect.collidepoint(event.pos):
                        button.process_click()
    def render(self,buttons,message):
        WINDOW.fill(BACKGROUND_COLOR)
        for box in self.boxes:
            box.draw()
        for button in buttons:
            button.draw()
        for die in self.dice:
            die.draw()
        message.display()
        pygame.display.flip()

    def reset(self, message):
        message.set_text(INITIAL_TEXT)
        for die in self.dice:
            die.value = 6

        for box in self.boxes:
            box.reset()

        for door in self.doors:
            self.doors[door] = False
        
        pass

    def request_roll_dice(self):
        if self.is_rolling or self.is_closing or self.should_reset or self.game_over!=0:
            return
        
        self.is_rolling = True
        pass

    def request_reset(self):
        if self.is_rolling or self.should_reset:
            return
        
        self.should_reset = True
        self.is_closing = False
        self.game_over = False

    def main_loop(self, message, buttons):
        while True:
            match self.game_screen:
                case 0:
                    self.menu()
                case 1:
                    self.rules_screen()
                case 2:
                    self.game_loop(message, buttons)


# ----- MAIN ----------

if __name__ == '__main__':
    # Setup
    pygame.init()
    WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption('RoubaChavePIX.exe')

    game = Game(9)
    message = Message(INITIAL_TEXT,FONT_SIZE_MESSAGE,MESSAGE_COLOR,bottomleft=(MESSAGE_X,MESSAGE_Y))
    button_roll = Button('Rolar',BUTTON_X,ROLL_BUTTON_Y,ROLL_BACK_COLOR,ROLL_TEXT_COLOR,game.request_roll_dice)
    button_reset = Button('Recomeçar', BUTTON_X, RESET_BUTTON_Y, RESET_BACK_COLOR, RESET_TEXT_COLOR, game.request_reset)
    buttons = [button_roll, button_reset]

    # Game loop
    game.reset(message)
    game.game_screen = 2
    game.main_loop(message, buttons)

        

        
