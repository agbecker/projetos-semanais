import pygame
import ui_elements as ui

if __name__ == '__main__':
    # Inicialização
    pygame.init()
    window = ui.WINDOW
    window.fill(ui.MAIN_BACKGROUND)

    calendar = ui.CalendarBox()
    elements = [calendar]

    for _ in range(1000):
        for e in elements:
            e.render()
        pygame.display.flip()

