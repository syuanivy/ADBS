#!/usr/bin/env python
from flask import Flask, jsonify, make_response, request, render_template, flash
from board import Board
from ship import Ship
from error import Error
from forms import ShootForm, ShipForm
app = Flask(__name__)


class Global:
    board = None


def _init_board():
    Global.board = Board(20, 20)


def _init_ships():
    """
    Initiate the board with two ships for now.
    """
    Global.board.add_ship(Ship(1, 1, 'horizontal', 3))
    Global.board.add_ship(Ship(10, 10, 'vertical', 5))


@app.route('/ship', methods=['GET', 'POST'])
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


@app.route('/shoot', methods=['GET', 'POST'])
def shoot():
    """
    Handle request to send an enemy battleship to a location on the map.
    """
    try:
        data = request.get_json()
        location = data['location']
        x = location['x']
        y = location['y']

    except KeyError:
        return Error(Error.ERR_OTHER, "Incomplete ship description").create_response()
    except:
        return Error(Error.ERR_OTHER).create_response()

    try:
        print [x, y]
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


@app.route('/', methods=['GET', 'POST'])
def main():
    _init_board()
    _init_ships()
    shoot_form = ShootForm(request.form)
    ship_form = ShipForm(request.form)
    # print shoot_form.errors
    # print ship_form.errors
    # if request.method == 'POST':
    #     name=request.form['name']
    #     print name
    #
    #     if shoot_form.validate():
    #         # Save the comment here.
    #         flash('Hello ' + name)
    #     else:
    #         flash('All the form fields are required. ')

    return render_template('game.html', shoot=shoot_form, ship=ship_form)

if __name__ == '__main__':

    app.run(host='127.0.0.1', port=5000, debug=True)


