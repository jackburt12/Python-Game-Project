import player
from flask import Flask, render_template, url_for, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///player.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), nullable=False)

    def __repr__(self):
        return '<Task %r>' % self.id

@app.route("/", methods=['POST', 'GET'])
def index():

    if request.method=='POST':
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
