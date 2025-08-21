# scenes.py
import pygame
import settings
from game_objects import adventurers_data, check_level_up
import random

def draw_hp_bar(surface, x, y, width, height, current_hp, max_hp):
    if current_hp < 0:
        current_hp = 0
    ratio = current_hp / max_hp
    background_rect = pygame.Rect(x, y, width, height)
    hp_rect = pygame.Rect(x, y, width * ratio, height)
    pygame.draw.rect(surface, (50, 50, 50), background_rect)
    pygame.draw.rect(surface, (0, 200, 0), hp_rect)
    pygame.draw.rect(surface, settings.BORDER_COLOR, background_rect, 2)

class Scene:
    def __init__(self):
        pass
    def handle_events(self, events):
        return None, None
    def update(self):
        pass
    def draw(self, screen):
        pass

class GuildHomeScene(Scene):
    def __init__(self):
        super().__init__()
        self.stage = 1
        self.adventurer_rects = []
        self.selected_adventurer_index = None
        self.gold = 100
        self.training_cost = 50
        self.message = ""
        self.message_timer = 0
        self.fonts = {
            "title": pygame.font.SysFont("meiryo", 60),
            "label": pygame.font.SysFont("meiryo", 40),
            "character": pygame.font.SysFont("meiryo", 32),
            "detail": pygame.font.SysFont("meiryo", 28)
        }
        self._create_ui_rects()

    def _create_ui_rects(self):
        margin = settings.SCREEN_WIDTH * 0.05
        self.list_panel_rect = pygame.Rect(margin, settings.SCREEN_HEIGHT * 0.15, settings.SCREEN_WIDTH * 0.4, settings.SCREEN_HEIGHT * 0.8)
        right_panel_x = self.list_panel_rect.right + margin
        report_width = settings.SCREEN_WIDTH - right_panel_x - margin
        self.report_rect = pygame.Rect(right_panel_x, self.list_panel_rect.y, report_width, settings.SCREEN_HEIGHT * 0.4)
        facility_y = self.report_rect.bottom + margin * 0.5
        facility_height = settings.SCREEN_HEIGHT - facility_y - (margin * 0.5)
        self.facility_rect = pygame.Rect(right_panel_x, facility_y, report_width, facility_height)

    def get_stage_number(self):
        return self.stage

    def process_battle_result(self, data):
        if data["result"] == "victory":
            self.stage += 1
            xp = data["xp_reward"]
            winner_name = data["winner_name"]
            self.message = f"冒険成功！ {winner_name}は{xp}の経験値を獲得！"
            self.message_timer = 180
            for adventurer in adventurers_data:
                if adventurer["name"] == winner_name:
                    adventurer["xp"] = adventurer.get("xp", 0) + xp
                    check_level_up(adventurer)
                    break
        else:
            self.message = "冒険は失敗に終わった..."
            self.message_timer = 180
    
    def handle_events(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.report_rect.collidepoint(event.pos):
                    if self.selected_adventurer_index is not None:
                        selected = adventurers_data[self.selected_adventurer_index]
                        return "BATTLE", {"player": selected}
                    else:
                        self.message = "冒険に出るメンバーを選択してください。"
                        self.message_timer = 120
                elif self.facility_rect.collidepoint(event.pos):
                    if self.selected_adventurer_index is not None:
                        adventurer = adventurers_data[self.selected_adventurer_index]
                        if self.gold >= self.training_cost:
                            self.gold -= self.training_cost
                            adventurer['attack'] += 2
                            self.message = f"{adventurer['name']}の攻撃力が上がった！"
                            self.message_timer = 120
                        else:
                            self.message = "ゴールドが足りません！"
                            self.message_timer = 120
                    else:
                        self.message = "先に冒険者を選択してください。"
                        self.message_timer = 120
                else:
                    for i, rect in enumerate(self.adventurer_rects):
                        if rect.collidepoint(event.pos):
                            self.selected_adventurer_index = i
                            return None, None
        return None, None

    def update(self):
        if self.message_timer > 0:
            self.message_timer -= 1
        else:
            self.message = ""

    def draw(self, screen):
        screen.fill(settings.DARK_GRAY)
        title_text = self.fonts["title"].render(f"ギルドホーム - Stage {self.stage}", True, settings.LIGHT_CYAN)
        title_rect = title_text.get_rect(center=(settings.SCREEN_WIDTH // 2, settings.SCREEN_HEIGHT * 0.08))
        screen.blit(title_text, title_rect)

        pygame.draw.rect(screen, settings.BORDER_COLOR, self.list_panel_rect, 2)
        list_label = self.fonts["label"].render("冒険者リスト", True, settings.LIGHT_CYAN)
        screen.blit(list_label, (self.list_panel_rect.x + 10, self.list_panel_rect.y + 10))
        self.adventurer_rects.clear()
        mouse_pos = pygame.mouse.get_pos()
        start_y = self.list_panel_rect.y + 60
        for i, adventurer in enumerate(adventurers_data):
            display_text = f"{adventurer['name']} - LV:{adventurer['level']}"
            text_color = settings.HIGHLIGHT_COLOR if i == self.selected_adventurer_index else settings.LIGHT_CYAN
            character_text = self.fonts["character"].render(display_text, True, text_color)
            text_rect = character_text.get_rect(topleft=(self.list_panel_rect.x + 10, start_y + (i * 40)))
            if text_rect.collidepoint(mouse_pos):
                pygame.draw.rect(screen, settings.BORDER_COLOR, text_rect, 2)
            screen.blit(character_text, text_rect)
            self.adventurer_rects.append(text_rect)
        
        pygame.draw.rect(screen, settings.BORDER_COLOR, self.report_rect, 2)
        detail_label = self.fonts["label"].render("冒険へ出発", True, settings.LIGHT_CYAN)
        screen.blit(detail_label, (self.report_rect.x + 10, self.report_rect.y + 10))
        if self.selected_adventurer_index is not None:
            adventurer = adventurers_data[self.selected_adventurer_index]
            details = [f"名前: {adventurer['name']}", f"LV: {adventurer['level']}", "", f"HP: {adventurer['hp']}", f"攻撃力: {adventurer['attack']}", f"防御力: {adventurer['defense']}"]
            detail_start_y = self.report_rect.y + 60
            for i, detail_line in enumerate(details):
                line_surface = self.fonts["detail"].render(detail_line, True, settings.LIGHT_CYAN)
                screen.blit(line_surface, (self.report_rect.x + 10, detail_start_y + (i * 30)))

        pygame.draw.rect(screen, settings.BORDER_COLOR, self.facility_rect, 2)
        facility_label = self.fonts["label"].render("施設：訓練所", True, settings.LIGHT_CYAN)
        screen.blit(facility_label, (self.facility_rect.x + 10, self.facility_rect.y + 10))
        cost_text = self.fonts["detail"].render(f"コスト: {self.training_cost} G", True, settings.LIGHT_CYAN)
        screen.blit(cost_text, (self.facility_rect.x + 10, self.facility_rect.y + 60))
        effect_text = self.fonts["detail"].render("効果: 攻撃力+2", True, settings.LIGHT_CYAN)
        screen.blit(effect_text, (self.facility_rect.x + 10, self.facility_rect.y + 90))

        gold_text = self.fonts["label"].render(f"所持金: {self.gold} G", True, settings.GOLD)
        gold_rect = gold_text.get_rect(topright=(settings.SCREEN_WIDTH - 30, 20))
        screen.blit(gold_text, gold_rect)

        if self.message:
            message_text = self.fonts["label"].render(self.message, True, settings.RED)
            message_rect = message_text.get_rect(center=(settings.SCREEN_WIDTH // 2, settings.SCREEN_HEIGHT - 50))
            screen.blit(message_text, message_rect)

class BattleScene(Scene):
    def __init__(self, player, enemy_pool):
        super().__init__()
        self.player = player.copy()
        self.enemy = random.choice(enemy_pool).copy()
        self.battle_log = [f"{self.enemy['name']}が現れた！"]
        self.battle_turn = "player"
        self.turn_timer = 120
        self.battle_result = None
        self.fonts = {"label": pygame.font.SysFont("meiryo", 40), "detail": pygame.font.SysFont("meiryo", 28)}

    def handle_events(self, events):
        if self.battle_result is not None and self.turn_timer <= 0:
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    return "GUILD_HOME", {"result": self.battle_result, "xp_reward": self.enemy.get("xp_reward", 0), "winner_name": self.player["name"]}
        return None, None

    def update(self):
        if self.battle_result is not None:
            if self.turn_timer > 0: self.turn_timer -= 1
            return
        if self.turn_timer > 0:
            self.turn_timer -= 1
            return
        if self.battle_turn == "player":
            log_message = f"▶ {self.player['name']}の攻撃！"
            damage = max(1, self.player['attack'] - self.enemy.get('defense', 0))
            self.enemy['hp'] -= damage
            log_message += f" {self.enemy['name']}に{damage}のダメージ！"
            self.battle_log.append(log_message)
            if self.enemy['hp'] <= 0:
                self.battle_result = "victory"
                self.battle_log.append("敵を倒した！ あなたの勝利です！")
                self.battle_log.append("（クリックしてギルドに戻る）")
                self.turn_timer = 60
            else:
                self.battle_turn = "enemy"
                self.turn_timer = 90
        elif self.battle_turn == "enemy":
            log_message = f"▶ {self.enemy['name']}の攻撃！"
            damage = max(1, self.enemy['attack'] - self.player.get('defense', 0))
            self.player['hp'] -= damage
            log_message += f" {self.player['name']}は{damage}のダメージを受けた。"
            self.battle_log.append(log_message)
            if self.player['hp'] <= 0:
                self.battle_result = "defeat"
                self.battle_log.append("あなたは倒された...")
                self.battle_log.append("（クリックしてギルドに戻る）")
                self.turn_timer = 60
            else:
                self.battle_turn = "player"
                self.turn_timer = 90
        if len(self.battle_log) > 6:
            self.battle_log.pop(0)

    def draw(self, screen):
        screen.fill(settings.DARK_GRAY)
        margin = settings.SCREEN_WIDTH * 0.05
        
        player_info_y = settings.SCREEN_HEIGHT * 0.1
        player_name_text = self.fonts["label"].render(f"{self.player['name']} LV:{self.player['level']}", True, settings.LIGHT_CYAN)
        screen.blit(player_name_text, (margin, player_info_y))
        draw_hp_bar(screen, margin, player_info_y + 50, 400, 30, self.player['hp'], self.player['max_hp'])

        enemy_info_x = settings.SCREEN_WIDTH - margin - 400
        enemy_name_text = self.fonts["label"].render(f"{self.enemy['name']}", True, settings.RED)
        screen.blit(enemy_name_text, (enemy_info_x, player_info_y))
        draw_hp_bar(screen, enemy_info_x, player_info_y + 50, 400, 30, self.enemy['hp'], self.enemy['max_hp'])

        log_height = settings.SCREEN_HEIGHT * 0.4
        log_y = settings.SCREEN_HEIGHT - log_height - (margin * 0.5)
        log_rect = pygame.Rect(margin, log_y, settings.SCREEN_WIDTH - (margin * 2), log_height)
        pygame.draw.rect(screen, settings.BORDER_COLOR, log_rect, 2)
        log_label_text = self.fonts["label"].render("バトルログ", True, settings.LIGHT_CYAN)
        screen.blit(log_label_text, (log_rect.x + 10, log_rect.y + 10))
        
        log_start_y = log_rect.y + 60
        for i, log in enumerate(reversed(self.battle_log)):
            log_y_pos = (log_rect.bottom - 30) - (i * 35)
            if log_y_pos < log_start_y:
                break
            log_text = self.fonts["detail"].render(log, True, settings.LIGHT_CYAN)
            screen.blit(log_text, (log_rect.x + 20, log_y_pos))