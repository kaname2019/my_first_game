# main.py
import pygame
import settings
from scenes import GuildHomeScene, BattleScene
def main():
    pygame.init()
    screen = pygame.display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
    pygame.display.set_caption(settings.CAPTION)
    clock = pygame.time.Clock()

    # ★★★ シーン管理のロジックを変更 ★★★
    guild_home_scene = GuildHomeScene()
    current_scene = guild_home_scene

    running = True
    while running:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
        
        # 現在のシーンにイベントを渡して、状態の変更をチェック
        next_scene_name, data = current_scene.handle_events(events)
        
        # もしシーンが変更されていたら
        if next_scene_name == "BATTLE":
            current_scene = BattleScene(data["player"], data["enemies"]) # 新しい戦闘シーンを作成
        
        current_scene.update()
        current_scene.draw(screen)
        
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    
if __name__ == '__main__':
    main()