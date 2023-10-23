import unittest
from io import StringIO
from unittest.mock import patch

from card_game import AttackCard, DefenseCard, DrawCard, Player, Enemy, Game, DiamondEnemy, SpadeEnemy

class TestCardGame(unittest.TestCase):

    def setUp(self):
        """
        Setup method to initialize cards, decks, player, and enemy for testing.
        """
        
        # Initialize cards for testing
        self.basic_attack = AttackCard("Attack", 1, 6, "Deal 6 damage to the enemy")
        self.double_attack = AttackCard("Double Attack", 2, 12, "Deal 12 damage to the enemy")
        self.basic_defense = DefenseCard("Defense", 1, 5, "Gain 5 defense points")
        self.double_defense = DefenseCard("Double Defense", 2, 10, "Gain 10 defense points")
        self.draw_card = DrawCard("Draw Card", 1, 1, "Draw 1 additional card")

        self.enemy_attack = AttackCard("Attack", 0, 6, "Deal 6 damage to the player")
        self.enemy_defense = DefenseCard("Defense", 0, 5, "Gain 5 defense points")

        # Player and Enemy deck initialization
        self.player_deck = [self.basic_attack, self.double_attack, self.basic_defense, self.double_defense, self.draw_card]
        self.enemy_deck = [self.enemy_attack, self.enemy_attack, self.enemy_attack, self.enemy_defense]

        # Player and Enemy initialization
        self.player = Player("Player", 30, deck=self.player_deck)
        self.enemy = Enemy("Enemy", 20, deck=self.enemy_deck)

    def test_attack_card(self):
        """
        Test if the attack card correctly reduces the enemy's HP.
        """
        initial_hp = self.enemy.current_hp
        self.basic_attack.play(self.player, self.enemy)
        self.assertEqual(self.enemy.current_hp, initial_hp - self.basic_attack.damage)

    def test_defense_card(self):
        """
        Test if the defense card correctly adds defense points to the player.
        """
        initial_defense = self.player.defense_point
        self.basic_defense.play(self.player, self.enemy)
        self.assertEqual(self.player.defense_point, initial_defense + self.basic_defense.defense_point)

    def test_draw_card(self):
        """
        Test if the draw card correctly increases the player's hand size.
        """
        initial_hand_size = len(self.player.hand_card)
        self.draw_card.play(self.player)
        self.assertEqual(len(self.player.hand_card), initial_hand_size + self.draw_card.draw_count)

    def test_character_take_damage(self):
        """
        Test if the player correctly takes damage considering defense points.
        """
        damage = 5
        initial_hp = self.player.current_hp
        initial_defense = self.player.defense_point
        self.player.take_damage(damage)
        self.assertEqual(self.player.current_hp, initial_hp - (damage - initial_defense))
        self.assertEqual(self.player.defense_point, 0)

    def test_character_add_defense(self):
        """
        Test if the defense points are correctly added to the character.
        """
        defense = 5
        initial_defense = self.player.defense_point
        self.player.add_defense(defense)
        self.assertEqual(self.player.defense_point, initial_defense + defense)

    def test_character_draw_additional_cards(self):
        """
        Test if the character correctly draws additional cards.
        """
        draw_count = 2
        initial_hand_size = len(self.player.hand_card)
        self.player.draw_additional_cards(draw_count)
        self.assertEqual(len(self.player.hand_card), initial_hand_size + draw_count)

    def test_player_display_card_list(self):
        """
        Test if the player displays card list correctly.
        """
        self.player.hand_card = [self.basic_attack, self.basic_defense]
        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.player.display_card_list()
            expected_output = "Your hand:\n1. Attack (AP: 1) - Deal 6 damage to the enemy\n2. Defense (AP: 1) - Gain 5 defense points\n"
            self.assertEqual(fake_out.getvalue(), expected_output)

    # def test_multiple_players_turn(self):
    #     """
    #     Test the player_turn method in the Game class for multiple players:
    #     1. Ensure each player's used cards and any remaining hand cards are moved to the used_card list at the end of their turn.
    #     2. Ensure each player draws a new hand up to their max_hand limit.
    #     3. Ensure each player's AP is reset to their maximum AP at the end of their turn.
    #     """

    #     # Create a simple game with two players and one enemy
    #     players = [
    #         Player("Player 1", 30, deck=self.player_deck),
    #         Player("Player 2", 30, deck=self.player_deck)
    #     ]
    #     enemies = [Enemy("Enemy", 20, deck=self.enemy_deck)]  # Adding one enemy here
    #     game = Game(players, enemies)

    #     # Mock user input to simulate player turns
    #     with patch('builtins.input', side_effect=["1", "END", "1", "END"]):
    #         for player in game.players:
    #             initial_used_card_count = len(player.used_card)
    #             initial_hand_card_count = len(player.hand_card)
    #             initial_ap = player.ap_max

    #             game.player_turn()

    #             # Check if used cards and any remaining hand cards are moved to the used_card list
    #             self.assertEqual(len(player.used_card), initial_used_card_count + initial_hand_card_count)

    #             # Check if each player draws a new hand up to their max_hand limit
    #             self.assertEqual(len(player.hand_card), player.max_hand)

    #             # Check if each player's AP is reset to their maximum AP at the end of their turn
    #             self.assertEqual(player.ap, initial_ap)

## TODO: Fix the hand_card[0] issue.
    # def test_multiple_enemies_turn(self):
    #     """
    #     Test the enemy_turn method in the Game class for multiple enemies:
    #     1. Ensure enemy use their card (assuming enemy always has only 1 card), unless it's being distracted skip_turn
    #     2. Ensure each enemy's used cards and any remaining hand cards are moved to the used_card list at the end of their turn.
    #     3. Ensure each enemy draws a new hand up to their max_hand limit.
    #     4. Ensure each enemy's AP is reset to their maximum AP at the end of their turn.
    #     """

    #     # Create a simple game with one player and two enemies
    #     players = [Player("Player", 30, deck=self.player_deck)]  # Adding one player here
    #     enemies = [
    #         SpadeEnemy("Enemy 1", 30, deck=self.enemy_deck),
    #         DiamondEnemy("Enemy 2", 30, deck=self.enemy_deck)
    #     ]
    #     game = Game(players, enemies)

    #     # Simulate each enemy's turn
    #     for enemy in game.enemies:
    #         initial_used_card_count = len(enemy.used_card)
    #         initial_hand_card_count = len(enemy.hand_card)
    #         initial_ap = enemy.ap_max

    #         # DiamondEnemy distracts SpadeEnemy
    #         if isinstance(enemy, DiamondEnemy):
    #             enemy.special_talent(game.enemies[0])

    #         game.enemy_turn()

    #         # Check if used cards and any remaining hand cards are moved to the used_card list
    #         self.assertEqual(len(enemy.used_card), initial_used_card_count + initial_hand_card_count)

    #         # Check if each enemy draws a new hand up to their max_hand limit
    #         self.assertEqual(len(enemy.hand_card), enemy.max_hand)

    #         # Check if each enemy's AP is reset to their maximum AP at the end of their turn
    #         self.assertEqual(enemy.ap, initial_ap)


if __name__ == "__main__":
    unittest.main()
