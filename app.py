import player
import random
from flask import Flask, render_template, url_for, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), nullable=False)
    location_x = db.Column(db.Integer, default = 0)
    location_y = db.Column(db.Integer, default = 0)

    local_location_x = Player.query.first().location_x
    local_location_y = Player.query.first().location_y

    def __repr__(self):
        return '<Task %r>' % self.id

    def is_alive(self):
        return self.hp > 0

    def do_action(self, action, **kwargs):
        action_method = getattr(self, action.method.__name__)
        if action_method:
            action_method(**kwargs)

    def print_inventory(self):
        for item in self.inventory:
            print(item, '\n')

    def move(self, dx, dy):
        self.local_location_x += dx
        self.local_location_y += dy
        print(world.tile_exists(self.local_location_x, self.local_location_y).intro_text())

    def move_north(self):
        self.move(dx=0, dy=-1)

    def move_south(self):
        self.move(dx=0, dy=1)

    def move_east(self):
        self.move(dx=1, dy=0)

    def move_west(self):
        self.move(dx=-1, dy=0)

    def attack(self, enemy):
        best_weapon = None
        max_dmg = 0
        for i in self.inventory:
            if isinstance(i, items.Weapon):
                if i.damage > max_dmg:
                    max_dmg = i.damage
                    best_weapon = i

        print("You use {} against {}!".format(best_weapon.name, enemy.name))
        enemy.hp -= best_weapon.damage
        if not enemy.is_alive():
            print("You killed {}!".format(enemy.name))
        else:
            print("{} HP is {}.".format(enemy.name, enemy.hp))

    def flee(self, tile):
        """Moves the player randomly to an adjacent tile"""
        available_moves = tile.adjacent_moves()
        r = random.randint(0, len(available_moves) - 1)
        self.do_action(available_moves[r])

@app.route("/", methods=['POST', 'GET'])
def index():

    if request.method=='POST':
        if 'new_game' in request.form:
            try:
                db.session.delete(Player.query.first())
                db.session.commit()
                return render_template("create-character.html")
            except:
                return 'There was an issue starting a new game!'

        player_name = request.form['name']
        player = Player(name=player_name)

        try:
            db.session.add(player)
            db.session.commit()
            return render_template("game-interface.html")
        except:
            return 'There was an issue creating the player'

    current_player = Player.query.first()
    if current_player is None:
        return render_template("create-character.html")
    else:
        return render_template("game-interface.html", player=current_player)

if __name__ == "__main__":
    app.run(debug=True)
