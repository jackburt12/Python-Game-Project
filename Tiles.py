import enemies

class MapTile:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def intro_text(self):
        raise NotImplementedError()
    def modify_player(self, player):
        raise NotImplementedError()

class StartingTile(MapTile):
    def intro_text(self):
        return """
        You have crash landed in the middle of a rainforest. You are the sole
        survivor. Armed only with your swiss army knife and a map, you are to
        find you way to the army basecamp and safety.
        """
    def modify_player(self, player):
        #room has no action on player
        pass

class LootTile(MapTile):
    def __init__(self, x, y, item):
        self.item = item
        super.()__init__(x, y)

    def add_loot(self, player):
        player.inventory.append(self.item)

    def modify_player(self, player):
        self.add_loot(player)

class EnemyTile(MapTile):
    def __init__(self, x, y, enemy):
        self.enemy = enemy
        super.()__init__(x,y)

    def modify_player(self, the_player):
        if self.enemy.is_alive():
            the_player.hp = the_player.hp - self.enemy.damage
            print("Enemy does {} damage. You have {} HP remaining.".format(self.enemy.damange, the_player.hp))

class EmptyForestPath(MapTile):
    def intro_text(self):
        return """
        Another unremarkable part of the forest, you must forge onwards.
        """
    def modify_player(self, player):
        #tile has no action on player
        pass

class EnemyCrocodile(EnemyTile):
      def __init__(self, x, y):
        super().__init__(x, y, enemies.Crocodile())

    def intro_text(self):
        if self.enemy.is_alive():
            return """
            A crocdile leaps from the river in a surprise attack!
            """
        else:
            return """
            The wounded crocodile retreats to the water for safety.
            """

class EnemyBear(EnemyTile):
      def __init__(self, x, y):
        super().__init__(x, y, enemies.Bear())

    def intro_text(self):
        if self.enemy.is_alive():
            return """
            A giant grizzly bear blocks your path and prepares to attack!
            """
        else:
            return """
            The dead bear lies on the ground, dead.
            """

class EnemyPython(EnemyTile):
      def __init__(self, x, y):
        super().__init__(x, y, enemies.Python())

    def intro_text(self):
        if self.enemy.is_alive():
            return """
            A python drops from a tree and wraps itself around your neck!
            """
        else:
            return """
            The wounded snake slithers away into the long grass.
            """

class EnemyHuman(EnemyTile):
      def __init__(self, x, y):
        super().__init__(x, y, enemies.Human())

    def intro_text(self):
        if self.enemy.is_alive():
            return """
            A lone tribe member stops you and attacks you with his spear!
            """
        else:
            return """
            The dead corpse rots on the ground.
            """

class FindFishTile(LootTile):
    def __init__(self, x, y):
        super().__init__(x, y, items.Fish())

    def intro_text(self):
        return """
        You stop by the river and take a little time to catch a fish.
        """

class StormTile(MapTile):
    def __init__(self, x, y):
        super.()__init__(x,y)

    def modify_player(self, the_player):
        the_player.hp = the_player.hp - self.storm.damange
        print("A heavy storm has started.")
        print("The storm inflicted {} damage. You have {} HP remaining".format(self.storm.damage, the_player.hp))

class SnakepitTile(MapTile):
    def __init__(self, x, y):
        super.()__init__(x,y)

    def modify_player(self, the_player):
        the_player.hp = the_player.hp - self.snakepit.damage
        print("You have fallen into a pit of deadly snakes!")
        print("The snakes have inflicted {} damage. You have {} HP remaining.".format(self.snakepit.damage, the_player.hp))
        
