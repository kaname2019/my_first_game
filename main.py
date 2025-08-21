# main.py
import pygame
import settings
from scenes import GuildHomeScene

def main():
    pygame.init()
    screen = pygame.display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
    pygame.display.set_caption(settings.CAPTION)
    clock = pygame.time.Clock()

    scene_manager = {
        "GUILD_HOME": GuildHomeScene()
    }
    current_scene = scene_manager["GUILD_HOME"]

    running = True
    while running:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
        
        current_scene.handle_events(events)
        current_scene.update()
        current_scene.draw(screen)
        
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == '__main__':
    main()