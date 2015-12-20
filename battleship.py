#!/usr/bin/env python
from flask import Flask, jsonify, make_response, request, render_template
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
    Place ships before the games if needed.
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
        x = int(request.form['x'])
        y = int(request.form['y'])
        direction = str(request.form['direction'])
        length = int(request.form['length'])
        new_ship = Ship(x, y, direction, length)
    except ValueError:
        return Error(Error.ERR_OTHER, "Invalid ship description").create_response()
    except IndexError:
        return Error(Error.ERR_INVALID_LOC).create_response()
    except:
        return Error(Error.ERR_OTHER).create_response()


    try:
        Global.board.add_ship(new_ship)
    except IndexError:
        return Error(Error.ERR_INVALID_LOC).create_response()
    except Error:
        return Error(Error.ERR_SHIP_COLLIDE).create_response()

    return make_response("The ship was successfully placed on the map.", 200)


@app.route('/shoot', methods=['GET', 'POST'])
def shoot():
    """
    Handle request to shoot a ship on the map.
    """
    try:
        x = int(request.form['x'])
        y = int(request.form['y'])
        if Global.board.has_ship(x, y):
            Global.board.sink_ship(x, y)
            if Global.board.numOfShips is 0:
                return make_response(jsonify({'result': 'Victory'}), 200)
            else:
                return make_response(jsonify({'result': 'Hit'}), 200)
        else:
            if Global.board.numOfShips is 0:
                return make_response(jsonify({'result': 'No ship on board'}), 200)
            else:
                return make_response(jsonify({'result': 'Miss'}), 200)
    except IndexError:
        return Error(Error.ERR_INVALID_LOC).create_response()
    except:
        return Error(Error.ERR_OTHER, 'A generic error occurred').create_response()


@app.route('/', methods=['GET', 'POST'])
def main():
    _init_board()
    shoot_form = ShootForm(request.form)
    ship_form = ShipForm(request.form)
    return render_template('game.html', shoot=shoot_form, ship=ship_form)

if __name__ == '__main__':

    app.run(host='0.0.0.0', port=5000, debug=True)


