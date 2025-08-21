# scenes.py
import pygame
import settings
import game_objects

class Scene: # (変更なし)
    pass

class GuildHomeScene(Scene):
    def __init__(self):
        super().__init__()
        print("ギルドホームシーンに切り替わりました。")
        self.adventurer_rects = []
        self.selected_adventurer_index = None
        self.gold = 100
        self.training_cost = 50
        self.message = ""
        self.message_timer = 0

        # UIの骨格となるRectを定義
        margin = settings.SCREEN_WIDTH * 0.05
        list_x = margin
        list_y = settings.SCREEN_HEIGHT * 0.15
        list_width = settings.SCREEN_WIDTH * 0.4
        list_height = settings.SCREEN_HEIGHT * 0.8
        self.list_panel_rect = pygame.Rect(list_x, list_y, list_width, list_height)
        
        right_panel_x = list_x + list_width + margin
        report_width = settings.SCREEN_WIDTH - right_panel_x - margin
        report_height = settings.SCREEN_HEIGHT * 0.4
        self.report_rect = pygame.Rect(right_panel_x, list_y, report_width, report_height)
        
        facility_y = list_y + report_height + margin * 0.5
        facility_height = settings.SCREEN_HEIGHT - facility_y - (margin * 0.5)
        self.facility_rect = pygame.Rect(right_panel_x, facility_y, report_width, facility_height)

        # フォントの準備
        self.title_font = pygame.font.SysFont("meiryo", 60)
        self.label_font = pygame.font.SysFont("meiryo", 40)
        self.character_font = pygame.font.SysFont("meiryo", 32)
        self.detail_font = pygame.font.SysFont("meiryo", 28)

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                for i, rect in enumerate(self.adventurer_rects):
                    if rect.collidepoint(event.pos):
                        self.selected_adventurer_index = i
                        return
                
                if self.facility_rect.collidepoint(event.pos):
                    if self.selected_adventurer_index is not None:
                        if self.gold >= self.training_cost:
                            self.gold -= self.training_cost
                            adventurer = game_objects.adventurers_data[self.selected_adventurer_index]
                            adventurer['attack'] += 2
                            self.message = f"{adventurer['name']}の攻撃力が上がった！"
                            self.message_timer = 120
                        else:
                            self.message = "ゴールドが足りません！"
                            self.message_timer = 120
                    else:
                        self.message = "先に冒険者を選択してください。"
                        self.message_timer = 120
    
    def update(self):
        if self.message_timer > 0:
            self.message_timer -= 1
        else:
            self.message = ""

    def draw(self, screen):
        screen.fill(settings.DARK_GRAY)

        # (A) タイトル
        title_text = self.title_font.render("ギルドホーム", True, settings.LIGHT_CYAN)
        title_rect = title_text.get_rect(center=(settings.SCREEN_WIDTH // 2, 50))
        screen.blit(title_text, title_rect)

        # (B) 冒険者リスト
        pygame.draw.rect(screen, settings.BORDER_COLOR, self.list_panel_rect, 2)
        list_label = self.label_font.render("冒険者リスト", True, settings.LIGHT_CYAN)
        screen.blit(list_label, (self.list_panel_rect.x + 10, self.list_panel_rect.y + 10))
        self.adventurer_rects.clear()
        mouse_pos = pygame.mouse.get_pos()
        start_y = self.list_panel_rect.y + 60
        for i, adventurer_data in enumerate(game_objects.adventurers_data):
            display_text = f"{adventurer_data['name']} - LV:{adventurer_data['level']}"
            text_color = settings.HIGHLIGHT_COLOR if i == self.selected_adventurer_index else settings.LIGHT_CYAN
            character_text = self.character_font.render(display_text, True, text_color)
            text_rect = character_text.get_rect(topleft=(self.list_panel_rect.x + 10, start_y + (i * 40)))
            if text_rect.collidepoint(mouse_pos):
                pygame.draw.rect(screen, settings.BORDER_COLOR, text_rect, 2)
            screen.blit(character_text, text_rect)
            self.adventurer_rects.append(text_rect)

        # (C) 詳細ステータス
        pygame.draw.rect(screen, settings.BORDER_COLOR, self.report_rect, 2)
        detail_label = self.label_font.render("詳細ステータス", True, settings.LIGHT_CYAN)
        screen.blit(detail_label, (self.report_rect.x + 10, self.report_rect.y + 10))
        if self.selected_adventurer_index is not None:
            adventurer = game_objects.adventurers_data[self.selected_adventurer_index]
            details = [f"名前: {adventurer['name']}", f"LV: {adventurer['level']}", "", f"HP: {adventurer['hp']}", f"攻撃力: {adventurer['attack']}", f"防御力: {adventurer['defense']}"]
            detail_start_y = self.report_rect.y + 60
            for i, detail_line in enumerate(details):
                line_surface = self.detail_font.render(detail_line, True, settings.LIGHT_CYAN)
                screen.blit(line_surface, (self.report_rect.x + 10, detail_start_y + (i * 30)))

        # (D) 施設：訓練所
        pygame.draw.rect(screen, settings.BORDER_COLOR, self.facility_rect, 2)
        facility_label = self.label_font.render("施設：訓練所", True, settings.LIGHT_CYAN)
        screen.blit(facility_label, (self.facility_rect.x + 10, self.facility_rect.y + 10))
        cost_text = self.detail_font.render(f"コスト: {self.training_cost} G", True, settings.LIGHT_CYAN)
        screen.blit(cost_text, (self.facility_rect.x + 10, self.facility_rect.y + 60))
        effect_text = self.detail_font.render("効果: 攻撃力+2", True, settings.LIGHT_CYAN)
        screen.blit(effect_text, (self.facility_rect.x + 10, self.facility_rect.y + 90))

        # (E) ゴールド表示
        gold_text = self.label_font.render(f"所持金: {self.gold} G", True, settings.GOLD)
        gold_rect = gold_text.get_rect(topright=(settings.SCREEN_WIDTH - 30, 20))
        screen.blit(gold_text, gold_rect)

        # (F) メッセージ表示
        if self.message:
            message_text = self.label_font.render(self.message, True, settings.RED)
            message_rect = message_text.get_rect(center=(settings.SCREEN_WIDTH // 2, settings.SCREEN_HEIGHT - 50))
            screen.blit(message_text, message_rect)