from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField

class ShootForm(Form):
    x = TextField('X coordinate:', validators=[validators.required()])
    y = TextField('Y coordinate:', validators=[validators.required()])


class ShipForm(Form):
    x = TextField('X coordinate:', validators=[validators.required()])
    y = TextField('Y coordinate:', validators=[validators.required()])
    direction = TextField('Direction:', validators=[validators.required()])
    length = TextField('Length:', validators=[validators.required()])


