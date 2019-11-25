class Inventory():
    """The base class for all items"""

    def __init__(self, items, damage, armour):
        self.items = items
        self.damage = damage
        self.armour = armour
