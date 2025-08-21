# scenes.py
import pygame
import settings
import game_objects

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
        self.adventurer_rects = []
        self.selected_adventurer_index = None # インデックス番号で選択を管理

        # フォントの準備
        self.title_font = pygame.font.SysFont("meiryo", 60)
        self.label_font = pygame.font.SysFont("meiryo", 40)
        self.character_font = pygame.font.SysFont("meiryo", 32)

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                for i, rect in enumerate(self.adventurer_rects):
                    if rect.collidepoint(event.pos):
                        self.selected_adventurer_index = i
                        print(f"{game_objects.adventurers_data[i]['name']}が選択されました。")
                        break

    def draw(self, screen):
        screen.fill(settings.DARK_GRAY)

        # (A) タイトル
        title_text = self.title_font.render("ギルドホーム", True, settings.LIGHT_CYAN)
        title_rect = title_text.get_rect(center=(settings.SCREEN_WIDTH // 2, 50))
        screen.blit(title_text, title_rect)

        # (B) 冒険者リスト
        list_label = self.label_font.render("冒険者リスト", True, settings.LIGHT_CYAN)
        screen.blit(list_label, (60, 110))

        self.adventurer_rects.clear() # 描画のたびにクリック範囲をリセット
        mouse_pos = pygame.mouse.get_pos()
        start_y = 160
        for i, adventurer_data in enumerate(game_objects.adventurers_data):
            display_text = f"{adventurer_data['name']} - LV:{adventurer_data['level']}"
            
            # 選択されているかで色を変える
            if i == self.selected_adventurer_index:
                text_color = settings.HIGHLIGHT_COLOR # 選択中はハイライト色
            else:
                text_color = settings.LIGHT_CYAN
                
            character_text = self.character_font.render(display_text, True, text_color)
            text_rect = character_text.get_rect(topleft=(60, start_y + (i * 40)))
            
            # マウスオーバーで枠線を描画
            if text_rect.collidepoint(mouse_pos):
                pygame.draw.rect(screen, settings.BORDER_COLOR, text_rect, 2)

            screen.blit(character_text, text_rect)
            self.adventurer_rects.append(text_rect)