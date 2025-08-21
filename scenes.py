# scenes.py
import pygame
import settings
import game_objects # game_objects.py の内容を読み込む

# 全てのシーンの基本となる「親」クラス
class Scene:
    def __init__(self):
        pass
    def handle_events(self, events):
        pass
    def update(self):
        pass
    def draw(self, screen):
        pass

# ギルドホーム画面のクラス
class GuildHomeScene(Scene):
    def __init__(self):
        super().__init__()
        print("ギルドホームシーンに切り替わりました。")

    def draw(self, screen):
        screen.fill(settings.DARK_GRAY)

        # (A) タイトル
        title_font = pygame.font.SysFont("meiryo", 60)
        title_text = title_font.render("ギルドホーム", True, settings.LIGHT_CYAN)
        title_rect = title_text.get_rect(center=(settings.SCREEN_WIDTH // 2, 50))
        screen.blit(title_text, title_rect)

        # (B) 冒険者リスト
        list_label_font = pygame.font.SysFont("meiryo", 40)
        list_label = list_label_font.render("冒険者リスト", True, settings.LIGHT_CYAN)
        screen.blit(list_label, (60, 110))

        character_font = pygame.font.SysFont("meiryo", 32)
        start_y = 160
        for i, adventurer_data in enumerate(game_objects.adventurers_data):
            display_text = f"{adventurer_data['name']} - LV:{adventurer_data['level']}"
            character_text = character_font.render(display_text, True, settings.LIGHT_CYAN)
            text_y = start_y + (i * 40)
            screen.blit(character_text, (60, text_y))