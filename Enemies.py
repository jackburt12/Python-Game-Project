class Enemy:
    """A base class for all enemies"""
    def __init__(self, name, hp, damage):
        """Creates a new enemy

        :param name: the name of the enemy
        :param hp: the hit points of the enemy
        :param damage: the damage the enemy does with each attack
        """
        self.name = name
        self.hp = hp
        self.damage = damage

    def is_alive(self):
        return self.hp > 0

class Storm:
    def __init__(self, name, damage):
        """Creates a storm
        :param name: the storm
        :param: damage: the damage the storm does at each tile
        """
        self.name = storm
        self.damage = 5

class Snakepit:
    def __init__(self, name, damage):
        """User falls into a snakepit"""
        self.name = snakepit
        self.damage = 20

class GrizzlyBear(Enemy):
    def __init__(self):
        super().__init__(name="Grizzly bear", hp=50, damage=10)

class Python(Enemy):
    def __init__(self):
        super().__init__(name="Python", hp=10, damage=5)

class Human(Enemy):
    def __init__(self):
        super().__init__(name="Human", hp=25, damage=10)

class Crocodile(Enemy):
    def __init__(self):
        super().__init__(name="Crocodile", hp=40, damage=20)
