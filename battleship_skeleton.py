#!/usr/bin/env python
from flask import Flask, jsonify, make_response, request, render_template, flash
import Tkinter
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField

app = Flask(__name__)

class Global:
    board = None


class Error:
    """
    Representation of error response from server.
    """
    ERR_OTHER = "ERR_OTHER"
    ERR_SHIP_COLLIDE = "ERR_SHIP_COLLIDE"
    ERR_INVALID_LOC = "ERR_INVALID_LOC"
    ERRS = {
        ERR_OTHER: "An unhandled error occurred",
        ERR_SHIP_COLLIDE: "A ship already exists on the map at this location",
        ERR_INVALID_LOC: "Invalid position on the map"
    }

    def __init__(self, code, message=None):
        """
        Create an error code with an optional message. If no message is provided
        the default value for that code is used instead. A ValueError is raised
        if the code is invalid.
        """
        if code not in Error.ERRS:
            raise ValueError("Invalid error code: %s" % code)
        self.code = code
        self.message = message

    def create_response(self):
        """
        Return a server response containing a JSON representation of the error.
        """
        if not self.message:
            message = Error.ERRS[self.code]
        else:
            message = self.message
        response = jsonify({'code': self.code, 'message': message})
        response.status_code = 400
        return response


class Ship:
    """
    Representation of a ship for the game.
    """
    DIRECTION_HORIZONTAL = "horizontal"
    DIRECTION_VERTICAL = "vertical"
    DIRECTIONS = [
        DIRECTION_HORIZONTAL,
        DIRECTION_VERTICAL
    ]
    LENGTH_MIN = 3
    LENGTH_MAX = 5

    def __init__(self, x, y, direction, length):
        """
        Create a ship with the specfied characteristics. A ValueError is raised
        if any of the arguments are invalid.
        """
        if direction not in Ship.DIRECTIONS:
            raise ValueError("Invalid ship direction: %s" % direction)
        length = int(length)
        if length < Ship.LENGTH_MIN or length > Ship.LENGTH_MAX:
            raise ValueError("Invalid ship length: %i" % length)
        self.x = int(x)
        self.y = int(y)
        self.direction = direction
        self.length = length

    def get_coordinates(self):
        """
        Returns the ship's position as a list of (x, y) tuples.
        """
        if self.direction == Ship.DIRECTION_HORIZONTAL:
            coordinates = [(x, self.y) for x in range(self.x, (self.x + self.length))]
        else:
            coordinates = [(self.x, y) for y in range((self.y + 1 - self.length), (self.y + 1))]
        return coordinates


class Board:
    """
    Representation of ships and their positions on a map.
    """
    def __init__(self, xsize, ysize):
        """
        Create a rectangular board with integer coordinates that range from
        (0, 0) to (xsize-1, ysize-1).
        """
        xsize = int(xsize)
        ysize = int(ysize)
        if xsize < 0 or ysize < 0:
            raise ValueError("Invalid board size: %s", ((xsize, ysize),))
        self.xsize = xsize
        self.ysize = ysize
        self._grid = [[None for y in range(ysize)] for x in range(xsize)]
        #self.show_board()

    def add_ship(self, ship):
        """
        Add a ship to the board. Raises an IndexError if the ship falls out of
        bounds.
        """
        if ship.x < 0 or ship.x >= self.xsize or ship.y < 0 or ship.y >= self.ysize:
            raise IndexError("Ship start position is not on board: %s" % ((ship.x, ship.y),))
        # Start with highest coordinate to get IndexError if out of bounds
        for x, y in reversed(sorted(ship.get_coordinates())):
            self._grid[x][y] = ship

    def query_coordinate(self, x, y):
        """
        Returns the ship that exists at the (x, y) coordinate on the board or
        None if there is no ship. Raises an IndexError if the coordinates fall
        out of bounds or a ValueError if the coordinates are not valid.
        """
        x = int(x)
        y = int(y)
        if x < 0 or x >= self.xsize or y < 0 or y >= self.ysize:
            raise IndexError("Position is not on board: %s" % ((x, y),))
        return self._grid[x][y]

    def show_board(self):
        root = Tkinter.Tk()
        canvas = Tkinter.Canvas(root)
        canvas.pack()

        for i in range(10):
            canvas.create_line(50 * i, 0, 50 * i, 400)
            canvas.create_line(0, 50 * i, 400, 50 * i)
        canvas.create_rectangle(100, 100, 200, 200, fill="blue")
        canvas.create_line(50, 100, 250, 200, fill="red", width=10)


@app.route('/ship', methods=['POST'])
def ship():
    """
    Handle request to send an enemy battleship to a location on the map.
    """
    try:
        data = request.get_json()
        location = data['location']
        x = location['x']
        y = location['y']
        direction = data['direction']
        length = data['length']
    except KeyError:
        return Error(Error.ERR_OTHER, "Incomplete ship description").create_response()
    except:
        return Error(Error.ERR_OTHER).create_response()

    try:
        ship = Ship(x, y, direction, length)
    except ValueError:
        return Error(Error.ERR_OTHER, "Invalid ship description").create_response()

    try:
        for x, y in ship.get_coordinates():
            if Global.board.query_coordinate(x, y):
                return Error(Error.ERR_SHIP_COLLIDE).create_response()
        Global.board.add_ship(ship)
    except IndexError:
        return Error(Error.ERR_INVALID_LOC).create_response()

    return make_response("", 200)


class ShootForm(Form):
    x = TextField('X coordinate:', validators=[validators.required()])
    y = TextField('Y coordinate:', validators=[validators.required()])


class ShipForm(Form):
    x = TextField('X coordinate:', validators=[validators.required()])
    y = TextField('Y coordinate:', validators=[validators.required()])
    direction = TextField('Direction:', validators=[validators.required()])
    length = TextField('Length:', validators=[validators.required()])


@app.route('/', methods=['GET', 'POST'])
def main():
    Global.board = Board(20, 20)
    shoot_form = ShootForm(request.form)
    ship_form = ShipForm(request.form)
    print shoot_form.errors
    print ship_form.errors
    if request.method == 'POST':
        name=request.form['name']
        print name

        if shoot_form.validate():
            # Save the comment here.
            flash('Hello ' + name)
        else:
            flash('All the form fields are required. ')

    return render_template('hello.html', shoot=shoot_form, ship=ship_form)

if __name__ == '__main__':

    app.run(host='127.0.0.1', port=5000, debug=True)


