# Import required modules
import random
from abc import ABC, abstractmethod
from relic import AttackBoostRelic
from game_display import clear_screen, display_separator

# Define Card classes
class Card(ABC):
    def __init__(self, name, ap, info, target_type='ENEMY'):
        self.name = name
        self.ap = ap
        self.info = info

    @abstractmethod
    def play(self, player, target):
        pass


class AttackCard(Card):
    def __init__(self, name, ap, damage, info):
        super().__init__(name, ap, info)
        self.damage = damage
        self.target_type = 'ENEMY'

    def play(self, player, target):
        # Calculate total damage including player's attack bonus
        total_damage = self.damage + player.attack
        target.take_damage(total_damage)
        print(f"{player.name} deals {total_damage} damage to {target.name} with {self.name}.")


class DefenseCard(Card):
    def __init__(self, name, ap, defense_point, info):
        super().__init__(name, ap, info)
        self.defense_point = defense_point
        self.target_type = 'ALLY'

    def play(self, player, target):
        player.add_defense(self.defense_point)


class DrawCard(Card):
    def __init__(self, name, ap, draw_count, info):
        super().__init__(name, ap, info)
        self.draw_count = draw_count
        self.target_type = 'ALLY'

    def play(self, player, target=None):
        player.draw_additional_cards(self.draw_count)

# Define Player and Enemy classes


class Character:
    def __init__(self, name, max_hp, ap=3, deck=None):
        self.name = name
        self.max_hp = max_hp
        self.current_hp = max_hp
        self.ap = ap
        self.ap_max = 3
        self.deck = deck if deck else []
        self.max_hand = 5
        self.hand_card = []
        self.used_card = []
        self.defense_point = 0
        self.money = 100
        self.experience = 0
        self.skip_turn = False
        self.attack = 0
        self.relics = []

    def take_damage(self, damage):
        damage_after_defense = max(0, damage - self.defense_point)
        self.defense_point = max(0, self.defense_point - damage)
        self.current_hp -= damage_after_defense

    def add_defense(self, defense_point):
        self.defense_point += defense_point

    def draw_additional_cards(self, draw_count):
        random.shuffle(self.deck)
        additional_cards = self.deck[:draw_count]
        self.hand_card.extend(additional_cards)

    def play_card(self, card, target):
        if card.ap <= self.ap:
            card.play(self, target)
            self.ap -= card.ap
            self.hand_card.remove(card)
            self.used_card.append(card)
        else:
            print("Not enough action points to play this card.")

    def add_relic(self, relic):
        """
        Add a relic to the character and apply its passive effect if applicable.
        """
        self.relics.append(relic)
        relic.apply_passive_effect(self)


class Player(Character):
    def display_card_list(self):
        display_separator()
        print("Your hand:")
        for i, card in enumerate(self.hand_card, 1):
            print(f"{i}. {card.name} (AP: {card.ap}) - {card.info}")


class Enemy(Character):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ap = 0  # Enemies have 0 action points
        self.ap_max = 0
        self.max_hand = 1
        self.cost = 0  # Add cost attribute for all enemies
        self.special_talent = None  # Add special_talent attribute for all enemies


class SpadeEnemy(Enemy):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cost = 50
        self.experience = 10


class DiamondEnemy(Enemy):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cost = 5
        self.experience = 5
        self.special_talent = self.distract

    def distract(self, target):
        print(f'{self.name} is chitchatting with {target.name}!')
        target.skip_turn = True


class HeartEnemy(Enemy):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cost = 25
        self.experience = 5


class ClubEnemy(Enemy):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cost = 100
        self.experience = 20

class Game:
    def __init__(self, players, enemies):
        self.players = players
        self.enemies = enemies

    def display_info(self):
        display_separator()
        for i, player in enumerate(self.players):
            print(
                f"Player {i + 1} HP: {player.current_hp}. Defense: {player.defense_point}")
        for i, enemy in enumerate(self.enemies):
            print(
                f"Enemy {i + 1} HP: {enemy.current_hp}. Defense: {enemy.defense_point}")
            print("Enemy Intent:", enemy.hand_card[0].info)
    
    def display_relics(self, player):
        display_separator()
        if player.relics:  # Check if the player has any relics
            print(f"{player.name} has the following relics and their effects:")
            for relic in player.relics:
                print(f"- {relic.name}: {relic.description}")

    def check_game_status(self):
        if any(player.current_hp <= 0 for player in self.players):
            print("Game Over. You lost.")
            return False

        if all(enemy.current_hp <= 0 for enemy in self.enemies):
            print("You WIN!!")
            return False

        return True

    def player_turn(self):
        for player in self.players:
            clear_screen()  # Clear the screen at the start of each player's turn
            print(f"\nIt's {player.name}'s turn!\n")
            input("Press Enter to continue...")

            # Move remaining cards in hand to used_card
            player.used_card.extend(player.hand_card)
            player.hand_card.clear()

            # Draw max_hand cards and reset AP to max
            player.draw_additional_cards(player.max_hand)
            player.ap = player.ap_max

            while True:
                self.display_info()
                self.display_relics(player)
                player.display_card_list()
                print(f"Action Points: {player.ap}")
                display_separator()

                user_input = input(
                    "Choose a card to play (by number) or type 'END' to end your turn: ")
                if user_input.upper() == "END":
                    break

                try:
                    card_number = int(user_input) - 1
                    if 0 <= card_number < len(player.hand_card):
                        card = player.hand_card[card_number]

                        # If the card is a DefenseCard, target your own team.
                        if isinstance(card, DefenseCard):
                            player_numbers = [str(i + 1)
                                              for i in range(len(self.players))]
                            target_player = input(
                                f"Choose a player to target ({', '.join(player_numbers)}): ")
                            if target_player in player_numbers:
                                target = self.players[int(target_player) - 1]
                                player.play_card(card, target)
                                print(
                                    f"{card.name} effect: {card.info} on {target.name}!")
                            else:
                                print("Invalid player number.")
                        else:
                            enemy_numbers = [str(i + 1)
                                             for i in range(len(self.enemies))]
                            target_enemy = input(
                                f"Choose an enemy to target ({', '.join(enemy_numbers)}): ")
                            if target_enemy in enemy_numbers:
                                target = self.enemies[int(target_enemy) - 1]
                                player.play_card(card, target)
                                print(
                                    f"{card.name} effect: {card.info} on {target.name}!")

                                # Check if enemy's HP is below 0 and remove from the game if true.
                                if target.current_hp <= 0:
                                    print(f"{target.name} has been defeated!")
                                    self.enemies.remove(target)
                            else:
                                print("Invalid enemy number.")
                    else:
                        print("Invalid card number.")
                except ValueError:
                    print(
                        "Invalid input. Please enter a number or type 'END' to end your turn.")
                
                user_input = input("Any key to continue...")
                clear_screen()  # Clear the screen at the start of each player's turn

    def enemy_turn(self):
        for enemy in self.enemies:
            print(f"\nIt's {enemy.name}'s turn!\n")
            input("Press Enter to continue...")

            if enemy.current_hp > 0:
                card = enemy.hand_card[0]
                if card.target_type == "ALLY":
                    target = random.choice(self.enemies)
                else:
                    target = random.choice(self.players)

                card.play(enemy, target)
                print(
                    f"\n{enemy.name} plays '{card.name}' against {target.name}!")
                print(f"{card.name} effect: {card.info} on {target.name}!\n")

                # Clean up Enemy card. Draw cards for the next round.
                enemy.used_card.extend(enemy.hand_card)
                enemy.hand_card.clear()

                # TODO: Enemy died, remove from the game.

    def game_loop(self):
        while True:
            for enemy in self.enemies:
                enemy.draw_additional_cards(1)
            if not self.check_game_status():
                break
            self.player_turn()
            if not self.check_game_status():
                break
            self.enemy_turn()


def main():
    # Initialize cards

    # Player cards
    basic_attack = AttackCard(
        "Attack", 1, 6, "Deal 6 damage to the enemy")
    double_attack = AttackCard(
        "Double Attack", 2, 12, "Deal 12 damage to the enemy")
    basic_defense = DefenseCard(
        "Defense", 1, 5, "Gain 5 defense points")
    double_defense = DefenseCard(
        "Double Defense", 2, 10, "Gain 10 defense points")
    draw_card = DrawCard("Draw Card", 0, 1, "Draw 1 additional card")
    draw_double_card = DrawCard(
        "Draw 2 Cards", 1, 2, "Draw 2 additional card")

    player_deck = [basic_attack, double_attack,
                   basic_defense, double_defense, draw_card]

    # Enemy cards
    enemy_attack = AttackCard("Attack", 0, 6, "Deal 6 damage to the player")
    enemy_defense = DefenseCard("Defense", 0, 5, "Gain 5 defense points")
    enemy_do_nothing = DefenseCard("Do nothing", 0, 0, "Enemy is wondering...")

    enemy_deck = [enemy_attack, enemy_attack,
                  enemy_attack, enemy_defense, enemy_do_nothing]

    # Initialize players and enemies
    player1 = Player("Player1", 30, deck=player_deck.copy())
    player2 = Player("Player2", 30, deck=player_deck.copy())

    # Add the AttackBoostRelic to player1
    player1.add_relic(AttackBoostRelic())

    diamond_enemy = DiamondEnemy("Diamond Enemy", 20, deck=enemy_deck.copy())
    spade_enemy = SpadeEnemy("Spade Enemy", 20, deck=enemy_deck.copy())

    players = [player1, player2]
    enemies = [diamond_enemy, spade_enemy]

    # Initialize and run the game
    game = Game(players, enemies)
    game.game_loop()


if __name__ == "__main__":
    main()
