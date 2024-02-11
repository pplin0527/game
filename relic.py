from abc import ABC, abstractmethod


class Relic(ABC):
    def __init__(self, name, description, active=False):
        self.name = name
        self.description = description
        self.active = active  # Indicates if the relic requires activation

    @abstractmethod
    def activate_effect(self, player):
        """
        Method to activate the relic's effect. This method should be overridden
        in subclasses for relics that have active effects.
        """
        pass

    def apply_passive_effect(self, player):
        """
        Method to apply the relic's passive effect. This method can be overridden
        in subclasses for relics that have passive effects.
        """
        pass


class AttackBoostRelic(Relic):
    def __init__(self, name="Warrior's Pendant", description="Increases player's attack by 2 points.", attack_bonus=2):
        super().__init__(name, description, active=False)
        self.attack_bonus = attack_bonus

    def activate_effect(self, player):
        """
        Placeholder method for active effects. This relic has no active effect,
        so this method does nothing.
        """
        pass  # No operation (no-op), since this relic does not have an active effect.

    def apply_passive_effect(self, player):
        """
        Apply the relic's passive effect by increasing the player's attack points.
        """
        player.attack += self.attack_bonus
        print(f"{self.name} applied: {player.name}'s attack increased by {self.attack_bonus} points.")
