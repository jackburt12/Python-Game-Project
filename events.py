import items, enemies, actions, world


class MapTile:
    """The base class for a tile within the world space"""
    def __init__(self, x, y):
        """Creates a new tile.

        :param x: the x-coordinate of the tile
        :param y: the y-coordinate of the tile
        """
        self.x = x
        self.y = y

    def intro_text(self):
        """Information to be displayed when the player moves into this tile."""
        raise NotImplementedError()

    def modify_player(self, the_player):
        """Process actions that change the state of the player."""
        raise NotImplementedError()

    def adjacent_moves(self):
        """Returns all move actions for adjacent tiles."""
        moves = []
        if world.tile_exists(self.x + 1, self.y):
            moves.append(actions.MoveEast())
        if world.tile_exists(self.x - 1, self.y):
            moves.append(actions.MoveWest())
        if world.tile_exists(self.x, self.y - 1):
            moves.append(actions.MoveNorth())
        if world.tile_exists(self.x, self.y + 1):
            moves.append(actions.MoveSouth())
        return moves

    def available_actions(self):
        """Returns all of the available actions in this room."""
        moves = self.adjacent_moves()
        moves.append(actions.ViewInventory())

        return moves



class StartingPoint(MapTile):
    def intro_text(self):
        return """
        You've crash landed in a treacherous rainforest. You are the sole
        survivor. Armed only with a map and your dagger, you are to find
        your way to basecamp and safety.
        """

    def modify_player(self, the_player):
        #Room has no action on player
        pass


class EmptyForestSquare(MapTile):
    def intro_text(self):
        return """
        Another unremarkable part of the forest. You must forge onwards.
        """

    def modify_player(self, the_player):
        #Room has no action on player
        pass


class LootRoom(MapTile):
    """A square that adds something to the player's inventory"""
    def __init__(self, x, y, item):
        self.item = item
        super().__init__(x, y)

    def add_loot(self, the_player):
        the_player.inventory.append(self.item)

    def modify_player(self, the_player):
        self.add_loot(the_player)


class FindBananaSquare(LootRoom):
    def __init__(self, x, y):
        super().__init__(x, y, items.Banana())

    def intro_text(self):
        return """
        You notice something edible hanging from a tree.
        It's a banana! You pick it.
        """


class FindOrangeSquare(LootRoom):
    def __init__(self, x, y):
        super().__init__(x, y, items.Orange(5))

    def intro_text(self):
        return """
        You notice something edible hanging from a tree.
        It's an orange! You pick it.
        """


class EnemySquare(MapTile):
    def __init__(self, x, y, enemy):
        self.enemy = enemy
        super().__init__(x, y)

    def modify_player(self, the_player):
        if self.enemy.is_alive():
            the_player.hp = the_player.hp - self.enemy.damage
            print("Enemy does {} damage. You have {} HP remaining.".format(self.enemy.damage, the_player.hp))

    def available_actions(self):
        if self.enemy.is_alive():
            return [actions.Flee(tile=self), actions.Attack(enemy=self.enemy)]
        else:
            return self.adjacent_moves()


class BearSquare(EnemySquare):
    def __init__(self, x, y):
        super().__init__(x, y, enemies.GrizzlyBear())

    def intro_text(self):
        if self.enemy.is_alive():
            return """
            A grizzly bear appears in front of you and snarls in preparation
            for an attack.
            """
        else:
            return """
            The corpse of the dead grizzly bear rots on the ground.
            """


class CrocodileSquare(EnemySquare):
    def __init__(self, x, y):
        super().__init__(x, y, enemies.Crocodile())

    def intro_text(self):
        if self.enemy.is_alive():
            return """
            A crocodile leaps out of the water in a surprise attack!
            """
        else:
            return """
            The wounded crocodile retreats to the water.
            """


class SnakeSquare(EnemySquare):
    def __init__(self, x, y):
        super().__init__(x, y, enemies.Python())

    def intro_text(self):
        if self.enemy.is_alive():
            return """
            A python drops from an overhead tree and wraps itself
            around your neck!
            """
        else:
            return """
            The python writhes in pain for a while, and then stops
            dead.
            """


class EagleSquare(EnemySquare):
    def __init__(self, x, y):
        super().__init__(x, y, enemies.Eagle())

    def intro_text(self):
        if self.enemy.is_alive():
            return """
            An eagle circles above and suddenly dives down in a surprise
            attack!
            """
        else:
            return """
            The wounded eagle flees to safety.
            """


class HunterSquare(EnemySquare):
    def __init__(self, x, y):
        super().__init__(x, y, enemies.Hunter())

    def intro_text(self):
        if self.enemy.is_alive():
            return """
            A native hunter appears from behind and attacks you with
            his spear!
            """
        else:
            return """
            The dead hunter coughs blood and lays dead on the ground, defeated.
            """


class LeaveCaveRoom(MapTile):
    def intro_text(self):
        return """
        You hear faint sounds of laughter and camaraderie in the distance...
        ... it grows as you get closer! It's the basecamp!


        Victory is yours!
        """

    def modify_player(self, player):
        player.victory = True
