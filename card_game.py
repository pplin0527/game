# Import required modules
import random
from abc import ABC, abstractmethod


# Define Card classes
class Card(ABC):
    def __init__(self, name, ap, info):
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

    def play(self, player, target):
        target.take_damage(self.damage)


class DefenseCard(Card):
    def __init__(self, name, ap, defense_point, info):
        super().__init__(name, ap, info)
        self.defense_point = defense_point

    def play(self, player, target):
        player.add_defense(self.defense_point)


class DrawCard(Card):
    def __init__(self, name, ap, draw_count, info):
        super().__init__(name, ap, info)
        self.draw_count = draw_count

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


class Player(Character):
    def display_card_list(self):
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
    def __init__(self):
        self.player = None
        self.enemy = None

    def create_characters(self):
        # Initialize player and enemy characters
        # The line below is removed since we initialize player and enemy later in the main function
        # self.player = Player("Player", 30, deck=[Card(...), ...])  # Add player's cards
        # self.enemy = Enemy("Enemy", 20, deck=[Card(...), ...])  # Add enemy's cards
        pass

    def display_info(self):
        print("\n" + "-" * 30)
        print(
            f"Player HP: {self.player.current_hp}. Defense: {self.player.defense_point}")
        print(
            f"Enemy HP: {self.enemy.current_hp}. Defense: {self.enemy.defense_point}")
        print("Enemy Intent:", self.enemy.hand_card[0].info)

    def check_game_status(self):
        if self.player.current_hp <= 0:
            print("Game Over. You lost.")
            return False

        if self.enemy.current_hp <= 0:
            print("You WIN!!")
            return False

        return True

    def player_turn(self):
        # Move remaining cards in hand to used_card
        self.player.used_card.extend(self.player.hand_card)
        self.player.hand_card.clear()

        self.player.draw_additional_cards(self.player.max_hand)
        self.player.ap = self.player.ap_max

        while True:
            self.display_info()
            self.player.display_card_list()
            print(f"Action Points: {self.player.ap}")

            user_input = input(
                "Choose a card to play (by number) or type 'END' to end your turn: ")
            if user_input.upper() == "END":
                break
            try:
                card_number = int(user_input) - 1
                if 0 <= card_number < len(self.player.hand_card):
                    self.player.play_card(
                        self.player.hand_card[card_number], self.enemy)
                    if not self.check_game_status():
                        break
                else:
                    print("Invalid card number.")
            except ValueError:
                print(
                    "Invalid input. Please enter a number or type 'END' to end your turn.")

    def enemy_turn(self):
        if self.enemy.skip_turn:
            self.enemy.skip_turn = False
        else:
            # Play existing hand_card (assuming only 1 card for enemy)
            self.enemy.hand_card[0].play(self.enemy, self.player)

            # Clean up Enemy card. Draw cards for the next round.
            self.enemy.used_card.extend(self.enemy.hand_card)
            self.enemy.hand_card.clear()

        return self.check_game_status()

    def game_loop(self):
        while True:
            self.enemy.draw_additional_cards(1)
            if not self.check_game_status():
                break
            self.player_turn()
            if not self.check_game_status():
                break
            self.enemy_turn()


def main():
    # Initialize cards

    # Player cards
    basic_attack = AttackCard("Attack", 1, 6, "Deal 6 damage to the enemy")
    double_attack = AttackCard(
        "Double Attack", 2, 12, "Deal 12 damage to the enemy")
    basic_defense = DefenseCard("Defense", 1, 5, "Gain 5 defense points")
    double_defense = DefenseCard(
        "Double Defense", 2, 10, "Gain 10 defense points")
    draw_card = DrawCard("Draw Card", 1, 1, "Draw 1 additional card")

    player_deck = [basic_attack, double_attack,
                   basic_defense, double_defense, draw_card]

    # Enemy cards
    enemy_attack = AttackCard("Attack", 0, 6, "Deal 6 damage to the player")
    enemy_defense = DefenseCard("Defense", 0, 5, "Gain 5 defense points")

    enemy_deck = [enemy_attack, enemy_attack, enemy_attack, enemy_defense]

    # Initialize and run the game
    game = Game()
    game.player = Player("Player", 30, deck=player_deck)
    game.enemy = DiamondEnemy("Diamond Enemy", 20, deck=enemy_deck)
    game.game_loop()


if __name__ == "__main__":
    main()
