import pygame
import ui_elements as ui
import data_structures as ds

if __name__ == '__main__':
    # Inicialização
    pygame.init()
    window = ui.WINDOW
    window.fill(ui.MAIN_BACKGROUND)

    # Calendar box
    calendar = ui.CalendarBox()
    lines = ui.ColumnLines()

    elements = [calendar, lines]

    # Main loop
    is_running = True
    while is_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False
        
        for e in elements:
            e.render()
        pygame.display.flip()
    
    pygame.quit()
