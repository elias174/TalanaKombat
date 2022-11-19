import json

from flask import Flask, jsonify, request
from marshmallow import ValidationError

from game_engine import GameEngine
from schemas import GameSchema

app = Flask(__name__)


@app.errorhandler(ValidationError)
def handle_error(err):
    """Return validation errors as JSON"""
    error_data = dict({'message': json.dumps(err.messages)})
    return error_data, 400


@app.route("/")
def hello_world():
    return "Talana Kombat"


@app.route('/game', methods=['POST'])
def game():
    game_data = GameSchema().load(request.get_json())
    game = GameEngine(player_info_j1=game_data['player1'], player_info_j2=game_data['player2'])
    return jsonify(
        {
            'narration': '\n'.join(game.get_narration_of_game())
        }
    )
