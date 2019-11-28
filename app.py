from items import GetItem, Weapon, Armour, Consumable
from inventory import Inventory
from scavenge import FoundItem, Scavenge
from flask import Flask, render_template, url_for, request, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy

#global variables
MOVEMENT_ENERGY_COST = 5
MOVEMENT_HUNGER_COST = 3
SCAVENGE_ENERGY_COST = 7
ENERGY_MESSAGE = "You fail to muster to strength to take even one more step, best find somewhere to sleep for the night..."
BOUNDARY_MESSAGE = "There are towering cliffs in front of you, you'll have to choose another direction..."

#setup flask and SQLAlchemy
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

#create the database model for the player
class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), nullable=False)
    health = db.Column(db.Integer, default=100)
    hunger = db.Column(db.Integer, default=81)
    energy = db.Column(db.Integer, default=100)
    location_x = db.Column(db.Integer, default=2)
    location_y = db.Column(db.Integer, default=3)

    def __repr__(self):
        return '<Task %r>' % self.id

#create the databse model for items
class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.String(32), nullable=False)
    item_type = db.Column(db.String(8), nullable=False)
    quantity = db.Column(db.Integer, default=1)

    def __repr__(self):
        return '<Task %r>' % self.id

@app.route("/", methods=['POST', 'GET'])
def index():

    #if this route has been accessed through a POST request, it will check why
    if request.method=='POST':

        #this block runs if the player has pressed the 'New Game' button
        if 'new_game' in request.form:
            try:
                clear_database()
                return render_template("create-character.html")
            except:
                return 'There was an issue starting a new game!'

        #this block runs if the player has just created a new chracter for the first time
        elif 'create_character' in request.form:
            player_name = request.form['name']
            player = Player(name=player_name)

            try:
                #clear the database just to check a new character is being created
                clear_database()

                #add any items you want the player to start with here:
                add_item(1, "Weapon")
                add_item(1, "Consumable")
                add_item(1, "Consumable")
                add_item(2, "Consumable")
                add_item(3, "Consumable")

                #add the player to the database
                db.session.add(player)
                db.session.commit()
                return render_template("game-interface.html", player=player, items=load_inventory())
            except:
                return 'There was an issue creating the player'

    #if this route has been accessed with a GET request, the game will start up as normal
    else:
        current_player = Player.query.first()
        if current_player is None:
            return render_template("create-character.html")
        else:
            return render_template("game-interface.html", player=current_player, items=load_inventory())

#the following are all of the routes for moving due to the player having pressed a
#direction on the compass. They simply all call the move_square method with the relevant direciton
#-------------------------------
@app.route("/north")
def north():
    return move_square("north")

@app.route("/east")
def east():
    return move_square("east")

@app.route("/south")
def south():
    return move_square("south")


@app.route("/west")
def west():
    return move_square("west")
#------------------------------

#if the player presses the sleep button this route will run
@app.route("/sleep")
def sleep():
    player = Player.query.first()

    #set player's energy to 100 and commit back to the database and send info to main.js
    player.energy = 100
    db.session.commit()
    return jsonify(energy=player.energy)

#if the player presses the scavenge button this route will run
@app.route("/scavenge")
def scavenge():
    player = Player.query.first()

    if player.energy - SCAVENGE_ENERGY_COST > 0:
        player.energy = player.energy-SCAVENGE_ENERGY_COST

        items = Scavenge(5)
        items_parsed = []

        for item in items:
            add_item(item.item_id, item.item_type)
            parsed_item = GetItem(item.item_type, item.item_id)
            items_parsed.append(parsed_item.name)
        return jsonify(result=items_parsed)
    else:
        return jsonify(error="You're too tired to scavenge for anything else")

#if the player selects any item in their inventory this route will run with (item) as a param
@app.route("/item/<item>")
def item(item):
    player = Player.query.first()

    #figures out what the item that has been selected is
    used_item = select_item(item)

    #checks if the item is a consumable
    #if it is a consumable it will check if it could take any effect (if the player is not full)
    #if so the item will be used and removed from the inventory
    if used_item.item_type == "Consumable":
        consumable = GetItem(used_item.item_type, used_item.item_id)

        old_stat = 0
        amount = 0

        #checks the consumable effect and executes based on hunger/health/energy
        if consumable.effect == "Hunger":
            #check that player is not full
            if player.hunger <100:
                #store what the stat is before consumable use
                old_stat = player.hunger
                #increase the stat by the necessary amount, however:
                #if the stat goes above the maximum (100) just set it to 100
                player.hunger = player.hunger + int(consumable.amount)
                if player.hunger > 100:
                    player.hunger = 100
                db.session.commit()
                #store the amount the stat changed by
                amount = player.hunger - old_stat
        #health/energy are functionally identical to the above, but changed for their relevant stat
        elif consumable.effect == "Health":
            if player.health <100:
                old_stat = player.health
                player.health = player.health + int(consumable.amount)
                if player.health > 100:
                    player.health = 100
                db.session.commit()
                amount = player.health - old_stat
        elif consumable.effect == "Energy":
            if player.energy <100:
                old_stat = player.energy
                player.energy = player.energy + int(consumable.amount)
                if player.energy > 100:
                    player.energy = 100
                db.session.commit()
                amount = player.energy - old_stat

        #if player is full on the relevant stat - return the error to the main.js file
        if amount is 0:
            return jsonify(error="Consumable would have no effect")
        else:
            return jsonify(hunger=player.hunger, health=player.health, energy=player.energy, effect=consumable.effect, amount=amount, quantity = decrease_quantity(used_item))

    #currently only consumables can be used
    #could check here to see if weapons/armour/materials are used if needed
    else:
        return "nothing"

#this method is called upon the game starting up in items=load_inventory() when returning the template
def load_inventory():
    #query all items in the players inventory from the database
    items_raw = Item.query.all()
    items_parsed = []
    #convert these items into more readable 'Item's
    #for example an item stored as item_id=1, item_type=Consumable would be converted
    #into a Consumable() object with a name = "Bag of Nuts", description, etc.
    for item in items_raw:
        print("Item type:" + item.item_type)
        print("Item id:" + item.item_id)
        new_item = GetItem(item.item_type, item.item_id)
        print(new_item)
        new_item.quantity = item.quantity
        items_parsed.append(new_item)

    #checks for the weapon and armour with the highest values
    #the value will be stored as the player's protection and damage ratings
    damage = 0
    armour = 0
    for item in items_parsed:
        if isinstance(item, Weapon):
            if int(item.damage) > int(damage):
                damage = item.damage
        elif isinstance(item, Armour):
            if int(item.protection) > int(armour):
                armour = item.protection

    return Inventory(items_parsed, damage, armour)

#parses a database item from an item name
#basically loops through inventory database and checks each item's name against the input param
def select_item(item_name):
    items_raw = Item.query.all()
    for item in items_raw:
        new_item = GetItem(item.item_type, item.item_id)
        if new_item.name == item_name:
            return item

#decreases the quantity of an item in the inventory on use
#if the quantity falls to zero, the item is deleted from the database
#and later removed from the list in main.js
def decrease_quantity(item):
    item.quantity = item.quantity-1
    if item.quantity <= 0:
        db.session.delete(item)
    db.session.commit()
    return item.quantity

#how the player moves is defined by this method
def move_square(direction):
    player = Player.query.first()

    #first checks the player has enough energy to move
    #if they don't an error will be returned to main.js
    if player.energy < MOVEMENT_ENERGY_COST:
        return jsonify(error=ENERGY_MESSAGE)
    else:
        #depending on the direction, the method checks if the desired movement
        #would move the user out of bounds, and if so returns an error message to main.js
        #otherwise the players location_x and location_y values are modified
        if direction is 'north':
            if (player.location_y>=11):
                return jsonify(error=BOUNDARY_MESSAGE)
            else:
                player.location_y = player.location_y + 1
        elif direction is 'east':
            if (player.location_x>=24):
                return jsonify(error=BOUNDARY_MESSAGE)
            else:
                player.location_x = player.location_x + 1
        elif direction is 'south':
            if (player.location_y<= 0):
                return jsonify(error=BOUNDARY_MESSAGE)
            else:
                player.location_y = player.location_y - 1
        elif direction is 'west':
            if (player.location_x<=0):
                return jsonify(error=BOUNDARY_MESSAGE)
            else:
                player.location_x = player.location_x - 1

    starving = "false"
    player.energy = player.energy - MOVEMENT_ENERGY_COST
    player.hunger = player.hunger - MOVEMENT_HUNGER_COST
    #after movement costs if their hunger falls to zero, they will suffer a health penalty
    if player.hunger < 0:
        player.hunger = 0
        player.health = player.health - 2
        starving = "true"
    db.session.commit()
    return jsonify(location="["+str(player.location_x)+", "+str(player.location_y)+"]", hunger=player.hunger, energy=player.energy, health=player.health, starving=starving)

#adds an item to the database given its id and type
def add_item(item_id, item_type):

    items = Item.query.all()
    #checks the database to see if the user already has at least one of the item
    #if they do the quantity will be increased rather than a new entry being created
    for item in items:
        if item.item_type == item_type and item.item_id == str(item_id):
            item.quantity = item.quantity + 1
            db.session.commit()
            return

    #if it is a brand new item it will be added and commited to the database
    new_item = Item(item_id=item_id, item_type=item_type)
    db.session.add(new_item)
    db.session.commit()

#completely clear the database of any items or players
def clear_database():
    db.session.query(Item).delete()
    db.session.query(Player).delete()
    db.session.commit()

if __name__ == "__main__":
    app.run(debug=True)
