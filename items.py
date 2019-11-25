import csv

class Item():
    """The base class for all items"""

    quantity = 0

    def __init__(self, name, description, value):
        self.name = name
        self.description = description
        self.value = value
        quantity = 1

class Weapon(Item):
    def __init__(self, name, description, value, damage):
        self.damage = damage
        super().__init__(name, description, value)

class Armour(Item):
    def __init__(self, name, description, value, protection):
        self.protection = protection
        super().__init__(name, description, value)

class Consumable(Item):
    def __init__(self, name, description, value, effect, amount):
        self.effect = effect
        self.amount = amount
        super().__init__(name, description, value)

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
        line_count = 0
        for row in csv_reader:
            name = row[0]
            print(name, flush=True)

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
