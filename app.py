from items import GetItem, Weapon, Armour
from inventory import Inventory
from flask import Flask, render_template, url_for, request, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), nullable=False)
    health = db.Column(db.Integer, default=100)
    hunger = db.Column(db.Integer, default=100)
    energy = db.Column(db.Integer, default=100)
    location_x = db.Column(db.Integer, default=2)
    location_y = db.Column(db.Integer, default=3)

    def __repr__(self):
        return '<Task %r>' % self.id

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.String(32), nullable=False)
    item_type = db.Column(db.String(8), nullable=False)
    quantity = db.Column(db.Integer, default=1)

    def __repr__(self):
        return '<Task %r>' % self.id

@app.route("/", methods=['POST', 'GET'])
def index():

    if request.method=='POST':
        if 'new_game' in request.form:
            try:
                clear_database()
                return render_template("create-character.html")
            except:
                return 'There was an issue starting a new game!'
        elif 'create_character' in request.form:
            player_name = request.form['name']
            player = Player(name=player_name)

            #this is how you add an item to the player
            #you must lookup the item you wish to add in its relevant csv file
            #whichever line it is in the csv file is what the item_id should be
            swiss = Item(item_id=1, item_type="Weapon")
            nuts = Item(item_id=1, item_type="Consumable")

            try:
                clear_database()
                db.session.add(player)
                db.session.add(swiss)
                db.session.add(nuts)
                db.session.commit()
                return render_template("game-interface.html", player=player, items=load_inventory())
            except:
                return 'There was an issue creating the player'
    else:
        current_player = Player.query.first()
        if current_player is None:
            return render_template("create-character.html")
        else:
            return render_template("game-interface.html", player=current_player, items=load_inventory())

@app.route("/north")
def north():
    print ("Went North")
    player = Player.query.first()
    if (player.location_y<11 and player.energy > 0):
        player.location_y = player.location_y + 1
        moved_square()
        db.session.commit()
        return jsonify(location="["+str(player.location_x)+", "+str(player.location_y)+"]", hunger=player.hunger, energy=player.energy)
    else:
        return "nothing"

@app.route("/east")
def east():
    print ("Went East")
    player = Player.query.first()
    if (player.location_x<24 and player.energy > 0):
        player.location_x = player.location_x + 1
        moved_square()
        db.session.commit()
        return jsonify(location="["+str(player.location_x)+", "+str(player.location_y)+"]", hunger=player.hunger, energy=player.energy)
    else:
        return "nothing"
@app.route("/south")
def south():
    print ("Went South")
    player = Player.query.first()
    if (player.location_y>0 and player.energy > 0):
        player.location_y = player.location_y - 1
        moved_square()
        db.session.commit()
        return jsonify(location="["+str(player.location_x)+", "+str(player.location_y)+"]", hunger=player.hunger, energy=player.energy)
    else:
        return "nothing"
@app.route("/west")
def west():
    print ("Went West")
    player = Player.query.first()
    if (player.location_x>0 and player.energy > 0):
        player.location_x = player.location_x - 1
        moved_square()
        db.session.commit()
        return jsonify(location="["+str(player.location_x)+", "+str(player.location_y)+"]", hunger=player.hunger, energy=player.energy)
    else:
        return "nothing"

def load_inventory():
    items_raw = Item.query.all()
    items_parsed = []
    for item in items_raw:
        new_item = GetItem(item.item_type, item.item_id)
        new_item.quantity = item.quantity
        items_parsed.append(new_item)

    damage = 0
    armour = 0

    for item in items_parsed:
        print(type(item))
        if isinstance(item, Weapon):
            print(item.damage)
            if int(item.damage) > int(damage):
                damage = item.damage
        elif isinstance(item, Armour):
            if int(item.protection) > int(armour):
                armour = item.protection

    return Inventory(items_parsed, damage, armour)

def moved_square():
    player = Player.query.first()
    player.hunger = player.hunger - 3
    player.energy = player.energy - 5

def clear_database():
    db.session.query(Item).delete()
    db.session.query(Player).delete()
    db.session.commit()

if __name__ == "__main__":
    app.run(debug=True)
