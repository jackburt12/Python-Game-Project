from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField

class Player:

    def __init__(self, name):
        self.name = name

    name = StringField('Name', validators=[DataRequired()])
    submit = SubmitField('Confirm')
