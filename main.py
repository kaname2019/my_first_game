# main.py
import pygame
import settings
import game_objects
from scenes import GuildHomeScene, BattleScene

def main():
    pygame.init()
    screen = pygame.display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
    pygame.display.set_caption(settings.CAPTION)
    clock = pygame.time.Clock()

    # シーンの管理
    guild_home_scene = GuildHomeScene()
    current_scene = guild_home_scene

    running = True
    while running:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
        
        next_scene_name, data = current_scene.handle_events(events)
        
        if next_scene_name == "BATTLE":
            stage = guild_home_scene.get_stage_number()
            
            if stage <= 3:
                enemy_pool = [e for e in game_objects.enemy_templates if e['name'] == 'スライム']
            elif stage <= 6:
                enemy_pool = [e for e in game_objects.enemy_templates if e['name'] in ['スライム', 'ゴブリン']]
            else:
                enemy_pool = game_objects.enemy_templates
                
            current_scene = BattleScene(data["player"], enemy_pool)
        elif next_scene_name == "GUILD_HOME":
            guild_home_scene.process_battle_result(data)
            current_scene = guild_home_scene
        
        current_scene.update()
        current_scene.draw(screen)
        
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == '__main__':
    main()