# scenes.py
import pygame
import settings

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