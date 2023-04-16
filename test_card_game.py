import unittest
from io import StringIO
from unittest.mock import patch

from card_game import AttackCard, DefenseCard, DrawCard, Player, Enemy, Game

# Paste your code here, without the `main()` function call at the end


class TestCardGame(unittest.TestCase):

    def setUp(self):
        # Initialize cards for testing
        self.basic_attack = AttackCard("Attack", 1, 6, "Deal 6 damage to the enemy")
        self.double_attack = AttackCard("Double Attack", 2, 12, "Deal 12 damage to the enemy")
        self.basic_defense = DefenseCard("Defense", 1, 5, "Gain 5 defense points")
        self.double_defense = DefenseCard("Double Defense", 2, 10, "Gain 10 defense points")
        self.draw_card = DrawCard("Draw Card", 1, 1, "Draw 1 additional card")

        self.enemy_attack = AttackCard("Attack", 0, 6, "Deal 6 damage to the player")
        self.enemy_defense = DefenseCard("Defense", 0, 5, "Gain 5 defense points")

        self.player_deck = [self.basic_attack, self.double_attack, self.basic_defense, self.double_defense, self.draw_card]
        self.enemy_deck = [self.enemy_attack, self.enemy_attack, self.enemy_attack, self.enemy_defense]

        self.player = Player("Player", 30, deck=self.player_deck)
        self.enemy = Enemy("Enemy", 20, deck=self.enemy_deck)

    def test_attack_card(self):
        initial_hp = self.enemy.current_hp
        self.basic_attack.play(self.player, self.enemy)
        self.assertEqual(self.enemy.current_hp, initial_hp - self.basic_attack.damage)

    def test_defense_card(self):
        initial_defense = self.player.defense_point
        self.basic_defense.play(self.player, self.enemy)
        self.assertEqual(self.player.defense_point, initial_defense + self.basic_defense.defense_point)

    def test_draw_card(self):
        initial_hand_size = len(self.player.hand_card)
        self.draw_card.play(self.player)
        self.assertEqual(len(self.player.hand_card), initial_hand_size + self.draw_card.draw_count)

    def test_character_take_damage(self):
        damage = 5
        initial_hp = self.player.current_hp
        initial_defense = self.player.defense_point
        self.player.take_damage(damage)
        self.assertEqual(self.player.current_hp, initial_hp - (damage - initial_defense))
        self.assertEqual(self.player.defense_point, 0)

    def test_character_add_defense(self):
        defense = 5
        initial_defense = self.player.defense_point
        self.player.add_defense(defense)
        self.assertEqual(self.player.defense_point, initial_defense + defense)

    def test_character_draw_additional_cards(self):
        draw_count = 2
        initial_hand_size = len(self.player.hand_card)
        self.player.draw_additional_cards(draw_count)
        self.assertEqual(len(self.player.hand_card), initial_hand_size + draw_count)

    def test_player_display_card_list(self):
        self.player.hand_card = [self.basic_attack, self.basic_defense]
        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.player.display_card_list()
            expected_output = "Your hand:\n1. Attack (AP: 1) - Deal 6 damage to the enemy\n2. Defense (AP: 1) - Gain 5 defense points\n"
            self.assertEqual(fake_out.getvalue(), expected_output)


if __name__ == "__main__":
    unittest.main
