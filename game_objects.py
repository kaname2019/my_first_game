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