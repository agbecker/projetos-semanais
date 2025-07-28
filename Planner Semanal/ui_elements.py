import pygame
from pygame import Color
import data_structures as ds

# Window Setting
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 1280*9//16
WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), flags=pygame.RESIZABLE)

# Constants
## Calendar Box
CALENDAR_BORDER_RATIO = 0.04
CALENDAR_CROP_RATIO = 0.7
CALENDAR_WIDTH = int(WINDOW_WIDTH*(1-2*CALENDAR_BORDER_RATIO))
CALENDAR_HEIGHT = int(WINDOW_HEIGHT*(1-2*CALENDAR_BORDER_RATIO))
CALENDAR_TOP = CALENDAR_BORDER_RATIO*WINDOW_HEIGHT
CALENDAR_LEFT = CALENDAR_BORDER_RATIO*WINDOW_WIDTH
CALENDAR_BOTTOM_FULL = WINDOW_HEIGHT-CALENDAR_TOP
CALENDAR_BOTTOM_CROPPED = CALENDAR_TOP + int(1-CALENDAR_CROP_RATIO)*WINDOW_HEIGHT
CALENDAR_CORNER_RADIUS = int(0.013*CALENDAR_WIDTH)

## Day Columns
COLUMN_WIDTH = CALENDAR_WIDTH//8
COLUMN_SEPARATOR_WIDTH = 2
COLUMN_SEPARATOR_HEIGHT = CALENDAR_HEIGHT*(1-2*CALENDAR_BORDER_RATIO)
COLUMN_SEPARATOR_TOP = CALENDAR_TOP + CALENDAR_HEIGHT//2 - COLUMN_SEPARATOR_HEIGHT//2
COLUMN_HEADER_TOP = COLUMN_SEPARATOR_TOP
COLUMN_HEADER_FONT_SIZE = 30

# Colors
CALENDAR_BACKGROUND = Color(245,245,250)
MAIN_BACKGROUND = Color(220,225,235)
COLUMN_SEPARATOR_COLOR = Color(200,205,214)
COLUMN_HEADER_COLOR = Color(120,140,180)

# Contém o calendário
class CalendarBox(object):
    def __init__(self):
        self.rect = pygame.Rect(CALENDAR_LEFT, CALENDAR_TOP, CALENDAR_WIDTH, CALENDAR_BOTTOM_FULL-CALENDAR_TOP)
        self.color = CALENDAR_BACKGROUND
        self.columns = [DayColumn(i) for i in range(7)]

    def render(self):
        pygame.draw.rect(WINDOW, self.color, self.rect, border_radius=CALENDAR_CORNER_RADIUS)
        for col in self.columns:
            col.render()

class DayColumn(object):
    def __init__(self, num):
        self.day = ds.Day(num)
        self.column = num
        self.is_selected = False
        self.header_font = pygame.font.Font(None, COLUMN_HEADER_FONT_SIZE)
        name = self.day.name
        self.x = CALENDAR_LEFT+(num+1)*COLUMN_WIDTH + COLUMN_WIDTH//2 - self.header_font.size(name)[0]//2
        self.header = self.header_font.render(name, True, COLUMN_HEADER_COLOR)

    def render(self):
        WINDOW.blit(self.header, (self.x, COLUMN_HEADER_TOP))

class ColumnLines(object):
    def __init__(self):
        self.xs = [CALENDAR_LEFT+i*COLUMN_WIDTH for i in range(1,7+1)]

    def render(self):
        end_y = COLUMN_SEPARATOR_TOP+COLUMN_SEPARATOR_HEIGHT
        for x in self.xs:
            pygame.draw.line(WINDOW,COLUMN_SEPARATOR_COLOR,(x,COLUMN_SEPARATOR_TOP),(x,end_y),COLUMN_SEPARATOR_WIDTH)

class TaskTag(object):
    def __init__(self, task):
        self.task = task