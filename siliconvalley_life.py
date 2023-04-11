import random

class Card:
    def __init__(self, name, ap, damage):
        self.name = name
        self.ap = ap
        # damage to hp; postive: attack, negative: defend
        self.damage = damage

class Character:
    def __init__(self, name, max_hp, deck):
        self.name = name
        self.max_hp = max_hp
        self.current_hp = max_hp
        self.ap = 3
        self.deck = deck
        self.hand = []
        self.used_cards = []

    def draw_cards(self, n=5):
        self.used_cards += self.hand
        while n > 0:
            curr_n = min(n, len(self.deck))
            self.hand = self.deck[:curr_n]
            del self.deck[:curr_n]
            n -= curr_n
            if len(self.deck) == 0:
                self.deck = self.used_cards
                random.shuffle(self.deck)
                self.used_cards.clear()
 
    def take_damage(self, damage):
        self.current_hp -= damage
        if self.current_hp < 0:
            self.current_hp = 0

    def is_dead(self):
        if self.current_hp == 0:
           print(f"{self.name} is DEAD")
        return self.current_hp == 0

    def play_card(self, card, target):
        target.take_damage(card.damage)
        self.ap -= card.ap
        self.used_cards.append(card)
        self.hand.remove(card)

class Enemy(Character):
    def __init__(self, name, max_hp, attack_value):
        super().__init__(name, max_hp, deck=[])
        self.attack_value = attack_value
        self.intent = None

    def choose_intent(self):
        intents = ["attack", "defend", "buff"]
        self.intent = random.choice(intents)

    def play_card(self, card, target):
        target.take_damage(card.damage)


def deal_damage(target, damage):
    target.take_damage(damage)

def display_hand(player):
    print("\nYour hand:")
    for i, card in enumerate(player.hand, 1):
        print(f"{i}. {card.name} (AP: {card.ap}, Damage: {card.damage})")


def display_available_cards(player):
    print("\nAvailable cards:")
    for i, card in enumerate(player.hand, 1):
        if player.ap >= card.ap:
            print(f"{i}. {card.name} (AP: {card.ap}, Damage: {card.damage})")


def display_status(player, enemy):
    print(f"\nAvailable AP: {player.ap}")
    print(f"{player.name} HP: {player.current_hp}/{player.max_hp}")
    print(f"{enemy.name} HP: {enemy.current_hp}/{enemy.max_hp}\n")


def player_turn(player, enemy):
    end_turn = False
    enemy.choose_intent()

    while player.ap > 0 and player.hand and not end_turn:
        if enemy.intent == "attack":
            print(f"{enemy.name}'s intent: {enemy.intent} for {enemy.attack_value} damage")
        elif enemy.intent == "defend":
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

            if chosen_card.ap > player.ap:
                print("Cannot use this card. No enough action points. Please enter another card number or 'end'.")
            else:
                if chosen_card.damage > 0:
                    print(f"-----> {player.name} attacking")
                    player.play_card(chosen_card, enemy)
                elif chosen_card.damage < 0:
                    print(f"-----> {player.name} defending")
                    player.play_card(chosen_card, player)
                display_status(player, enemy)
        else:
            print("Invalid input. Please enter a valid card number or 'end'.")


def enemy_turn(player, enemy):
    if enemy.intent == "attack":
        print(f"-----> {enemy.name} attacking")
        enemy.play_card(Card("Enemy Attack", 0, enemy.attack_value), player)
    elif enemy.intent == "defend":
        print(f"-----> {enemy.name} defending")
        enemy.play_card(Card("Enemy Defense", 0, -enemy.attack_value), enemy)
    else:
        print(f"-----> {enemy.name} doing nothing")


def main():
    attack = Card("Attack", 1, 6)
    double_attack = Card("Double Attack", 2, 12)
    defense = Card("Defense", 1, -5)
    double_defense = Card("Double Defense", 2, -10)  # Add your desired effect for "Double Defense"

    deck = [attack, attack, attack, attack, double_attack, defense, defense, defense, defense, double_defense]
    random.shuffle(deck)

    player = Character("Player", 50, deck)
    enemy = Enemy("Goblin", 25, 8)

    round_number = 1

    while not player.is_dead() and not enemy.is_dead():
        print(f"\n******** Round {round_number} ********")
        player.ap = 3
        player.draw_cards()

        display_hand(player)
        display_status(player, enemy)

        player_turn(player, enemy)
        if enemy.is_dead():
            break
        enemy_turn(player, enemy)

        display_status(player, enemy)
        round_number += 1


if __name__ == "__main__":
    main()
