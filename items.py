import csv

class Item():
    """The base class for all items"""

    quantity = 0

    def __init__(self, name, description, value):
        self.name = name
        self.description = description
        self.value = value
        quantity = 1

    def serialize(self):
        return {
            'name': self.name,
            'description': self.description,
            'value': self.value,
            'quantity': self.quantity
        }

class Weapon(Item):
    def __init__(self, name, description, value, damage):
        self.damage = damage
        super().__init__(name, description, value)

    def serialize(self):
        return {
            'name': self.name,
            'description': self.description,
            'value': self.value,
            'quantity': self.quantity,
            'damage': self.damage
        }

class Armour(Item):
    def __init__(self, name, description, value, protection):
        self.protection = protection
        super().__init__(name, description, value)

    def serialize(self):
        return {
            'name': self.name,
            'description': self.description,
            'value': self.value,
            'quantity': self.quantity,
            'protection': self.protection
        }

class Consumable(Item):
    def __init__(self, name, description, value, effect, amount):
        self.effect = effect
        self.amount = amount
        super().__init__(name, description, value)

    def serialize(self):
        return {
            'name': self.name,
            'description': self.description,
            'value': self.value,
            'quantity': self.quantity,
            'effect': self.effect,
            'amount': self.amount

        }

def GetItem(item_type, item_id):
    file = ""
    if item_type == "Weapon":
        file = "resources/weapons.csv"
    elif item_type == "Armour":
        file = "resources/armour.csv"
    elif item_type == "Consumable":
        file = "resources/consumables.csv"
    elif item_type == "Material":
        file = "resources/materials.csv"


    with open(file) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        rows = list(csv_reader)

        row = rows[int(item_id)-1]

        name = row[0]

        description = row[1]
        value = row[2]

        if item_type == "Weapon":
            damage = row[3]
            return Weapon(name, description, value, damage)
        elif item_type == "Armour":
            protection = row[3]
            return Armour(name, description, value, protection)

        elif item_type == "Consumable":
            effect = row[3]
            amount = row[4]
            return Consumable(name, description, value, effect, amount)

        else:
            return Item(name, description, value)
