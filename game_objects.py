# game_objects.py
import pygame

# 冒険者の設計図（クラス）
class Adventurer:
    def __init__(self, name, level, hp, attack, defense):
        self.name = name
        self.level = level
        self.hp = hp
        self.attack = attack
        self.defense = defense
        # 冒険者の初期データ
adventurers_data = [
    {"name": "アタリ", "level": 5, "hp": 150, "attack": 30, "defense": 20},
    {"name": "ベータ", "level": 3, "hp": 90, "attack": 15, "defense": 10},
    {"name": "シーラ", "level": 4, "hp": 120, "attack": 10, "defense": 15}
]