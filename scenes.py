# scenes.py
import pygame
import settings
from game_objects import adventurers_data, check_level_up
import random

# HPバーを描画する関数
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
        # ... (既存の変数は変更なし) ...
        self.adventurer_rects = []
        self.selected_adventurer_index = None
        self.gold = 100
        # ...

        # フォントの準備
        self.title_font = pygame.font.SysFont("meiryo", 60)
        self.label_font = pygame.font.SysFont("meiryo", 40)
        self.character_font = pygame.font.SysFont("meiryo", 32)
        self.detail_font = pygame.font.SysFont("meiryo", 28)

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.report_rect.collidepoint(event.pos):
                    if self.selected_adventurer_index is not None:
                        selected = game_objects.adventurers_data[self.selected_adventurer_index]
                        return "BATTLE", {"player": selected, "enemies": game_objects.enemy_templates}
                    else:
                        self.message = "冒険に出るメンバーを選択してください。"
                        self.message_timer = 120
                # ... (他のクリック判定は変更なし) ...
        return None, None
    
    # ★★★ 新しいメソッド：戦闘結果を処理する ★★★
    def process_battle_result(self, data):
        if data["result"] == "victory":
            xp = data["xp_reward"]
            self.message = f"冒険成功！ {xp} の経験値を獲得！"
            self.message_timer = 180 # 3秒表示
            # 経験値を加算するロジックはここに追加していく
        else:
            self.message = "冒険は失敗に終わった..."
            self.message_timer = 180
    
    # (update, drawメソッドは変更なし)
    # ...

# ★★★ 戦闘シーンクラス（大幅に機能追加） ★★★
class BattleScene(Scene):
    def __init__(self, player, enemy_templates):
        super().__init__()
        self.player = player.copy()
        self.enemy = random.choice(enemy_templates).copy()
        
        self.battle_log = [f"{self.enemy['name']}が現れた！"]
        self.battle_turn = "player"
        self.turn_timer = 120
        self.battle_result = None # ★ "victory", "defeat", or None

        # フォントの準備
        self.label_font = pygame.font.SysFont("meiryo", 40)
        self.detail_font = pygame.font.SysFont("meiryo", 28)

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
        # 戦闘が終了していたら、クリックでギルドホームに戻る
        if self.battle_result is not None:
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # シーン変更の合図と、戦闘結果を返す
                    return "GUILD_HOME", {"result": self.battle_result, "xp_reward": self.enemy.get("xp_reward", 0)}
        return None, None
    
    def process_battle_result(self, data):
        if data["result"] == "victory":
            xp = data["xp_reward"]
            winner_name = data["winner_name"]
            self.message = f"冒険成功！ {winner_name}は{xp}の経験値を獲得！"
            self.message_timer = 180
            for adventurer in adventurers_data:
                if adventurer["name"] == winner_name:
                    adventurer["xp"] += xp
                    check_level_up(adventurer)
                    break
        else:
            self.message = "冒険は失敗に終わった..."
            self.message_timer = 180
            
    def update(self):
        # 戦闘が既に終了していたら、何もしない
        if self.battle_result is not None:
            return

        if self.turn_timer > 0:
            self.turn_timer -= 1
            return

        # プレイヤーのターン
        if self.battle_turn == "player":
            log_message = f"▶ {self.player['name']}の攻撃！"
            damage = max(1, self.player['attack'] - self.enemy['defense'])
            self.enemy['hp'] -= damage
            log_message += f" {self.enemy['name']}に {damage} のダメージを与えた。"
            self.battle_log.append(log_message)
            self.battle_turn = "enemy"
            self.turn_timer = 90
        
        # 敵のターン
        elif self.battle_turn == "enemy":
            log_message = f"▶ {self.enemy['name']}の攻撃！"
            damage = max(1, self.enemy['attack'] - self.player['defense'])
            self.player['hp'] -= damage
            log_message += f" {self.player['name']}は {damage} のダメージを受けた。"
            self.battle_log.append(log_message)
            self.battle_turn = "player"
            self.turn_timer = 90

        if len(self.battle_log) > 6:
            self.battle_log.pop(0)

        # ★★★ 勝敗判定 ★★★
        if self.enemy['hp'] <= 0:
            self.battle_result = "victory"
            self.battle_log.append("敵を倒した！ あなたの勝利です！")
            self.battle_log.append("（クリックしてギルドに戻る）")
        elif self.player['hp'] <= 0:
            self.battle_result = "defeat"
            self.battle_log.append("あなたは倒された...")
            self.battle_log.append("（クリックしてギルドに戻る）")

    def draw(self, screen):
        # (描画コードは変更なし)
        pass