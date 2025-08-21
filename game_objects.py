# game_objects.py
import pygame
import time

class Adventurer:
    def __init__(self, name, level, hp, attack, defense):
        self.name = name
        self.level = level
        self.hp = hp
        self.attack = attack
        self.defense = defense

adventurers_data = [
    {"name": "アタリ", "level": 1, "xp": 0, "xp_to_next_level": 50, "hp": 150, "max_hp": 150, "attack": 15, "defense": 8, "skills": ["強打", "ヒール"]},
    {"name": "ベータ", "level": 1, "xp": 0, "xp_to_next_level": 50, "hp": 90, "max_hp": 90, "attack": 15, "defense": 10, "skills": ["ファイア", "ヒール"]},
    {"name": "シーラ", "level": 1, "xp": 0, "xp_to_next_level": 50, "hp": 120, "max_hp": 120, "attack": 10, "defense": 15, "skills": ["ヒール", "防御"]}
]

enemy_templates = [
    {"name": "スライム", "hp": 50, "max_hp": 50, "attack": 8, "defense": 3, "xp_reward": 25},
    {"name": "ゴブリン", "hp": 80, "max_hp": 80, "attack": 12, "defense": 5, "xp_reward": 40},
    {"name": "オーク",   "hp": 150, "max_hp": 150, "attack": 15, "defense": 8, "xp_reward": 70},
    {"name": "ゴーレム", "hp": 250, "max_hp": 250, "attack": 18, "defense": 15, "xp_reward": 120}
]

def check_level_up(player):
    if player.get('xp', 0) >= player.get('xp_to_next_level', 9999):
        player['level'] += 1
        player['xp'] -= player['xp_to_next_level']
        player['xp_to_next_level'] = int(player['xp_to_next_level'] * 1.5)
        player['max_hp'] += 20
        player['attack'] += 5
        player['defense'] += 3
        player['hp'] = player['max_hp']
        print(f"★★ {player['name']}はレベルアップ！ ★★")