import random

class Card:
    def __init__(self, name, cost, ap, effect):
        self.name = name
        self.cost = cost
        self.ap = ap
        self.effect = effect

    def play(self, target):
        self.effect(target)

class Character:
    def __init__(self, name, max_hp, deck):
        self.name = name
        self.max_hp = max_hp
        self.current_hp = max_hp
        self.energy = 3
        self.ap = 3
        self.deck = deck
        self.hand = []
        self.used_cards = []

    def draw_cards(self, n=5):
        if len(self.deck) < n:
            self.deck.extend(self.used_cards)
            self.used_cards.clear()
            random.shuffle(self.deck)

        self.hand = random.sample(self.deck, n)
        for card in self.hand:
            self.deck.remove(card)

    def take_damage(self, damage):
        self.current_hp -= damage
        if self.current_hp < 0:
            self.current_hp = 0

    def is_dead(self):
        return self.current_hp == 0

    def play_card(self, card, target):
        if self.energy >= card.cost and self.ap >= card.ap:
            card.play(target)
            self.energy -= card.cost
            self.ap -= card.ap
            self.used_cards.append(card)

class Enemy(Character):
    def __init__(self, name, max_hp, attack_value):
        super().__init__(name, max_hp, deck=[])
        self.attack_value = attack_value
        self.intent = None

    def choose_intent(self):
        intents = ["attack", "defend", "buff"]
        self.intent = random.choice(intents)

def deal_damage(target, damage):
    target.take_damage(damage)

def display_hand(player):
    print("\nYour hand:")
    for i, card in enumerate(player.hand, 1):
        print(f"{i}. {card.name} (AP: {card.ap}, Cost: {card.cost})")


def display_available_cards(player):
    print("\nAvailable cards:")
    for i, card in enumerate(player.hand, 1):
        if player.ap >= card.ap and player.energy >= card.cost:
            print(f"{i}. {card.name} (AP: {card.ap}, Cost: {card.cost})")


def display_status(player, enemy):
    print(f"\nAvailable AP: {player.ap}")
    print(f"{player.name} HP: {player.current_hp}/{player.max_hp}")
    print(f"{enemy.name} HP: {enemy.current_hp}/{enemy.max_hp}")


def player_turn(player, enemy):
    end_turn = False

    while player.ap > 0 and player.hand and not end_turn:
        enemy.choose_intent()
        if enemy.intent == "attack":
            print(f"{enemy.name}'s intent: {enemy.intent} for {enemy.attack_value} damage")
        else:
            print(f"{enemy.name}'s intent: {enemy.intent}")

        display_available_cards(player)

        card_choice = input("Choose a card number to play, or type 'end' to end your turn: ").lower()

        if card_choice == "end":
            end_turn = True
            break

        if card_choice.isdigit() and 1 <= int(card_choice) <= len(player.hand):
            chosen_card = player.hand[int(card_choice) - 1]

            if chosen_card.name.startswith("Attack"):
                player.play_card(chosen_card, enemy)
                player.hand.remove(chosen_card)
            elif chosen_card.name.startswith("Defense"):
                player.play_card(chosen_card, player)
                player.hand.remove(chosen_card)

            display_status(player, enemy)
        else:
            print("Invalid input. Please enter a valid card number or 'end'.")


def enemy_turn(player, enemy):
    if enemy.intent == "attack":
        enemy.play_card(Card("Enemy Attack", 0, 0, lambda target: deal_damage(target, enemy.attack_value)), player)


def main():
    attack = Card("Attack", 1, 1, lambda target: deal_damage(target, 6))
    double_attack = Card("Double Attack", 2, 2, lambda target: deal_damage(target, 12))
    defense = Card("Defense", 1, 1, lambda target: None)  # Add your desired effect for "Defense"
    double_defense = Card("Double Defense", 2, 2, lambda target: None)  # Add your desired effect for "Double Defense"

    deck = [attack, attack, attack, attack, double_attack, defense, defense, defense, defense, double_defense]

    player = Character("Player", 50, deck)
    enemy = Enemy("Goblin", 25, 8)

    round_number = 1

    while not player.is_dead() and not enemy.is_dead():
        print(f"\nRound {round_number}")
        player.ap = 3
        player.draw_cards()

        display_hand(player)
        display_status(player, enemy)

        player_turn(player, enemy)
        enemy_turn(player, enemy)

        display_status(player, enemy)
        round_number += 1


if __name__ == "__main__":
    main()
