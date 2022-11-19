from marshmallow import Schema, fields, post_load

from constants import MOVEMENTS_COMBO_J1, MOVEMENTS_COMBO_J2
from game_engine import PlayerInfo


class PlayerSchema(Schema):
    name = fields.Str(required=True)
    moves = fields.List(fields.String(), required=True)
    strikes = fields.List(fields.String(), required=True)

    @post_load
    def make_player_info(self, data, **kwargs):
        player_object = PlayerInfo(**data, damage_combos=dict())
        return player_object


class GameSchema(Schema):

    player1 = fields.Nested(PlayerSchema(), required=True)
    player2 = fields.Nested(PlayerSchema(), required=True)

    @post_load
    def make_data_game(self, data, **kwargs):
        data['player1'].combos_mapping_movements = MOVEMENTS_COMBO_J1
        data['player2'].combos_mapping_movements = MOVEMENTS_COMBO_J2
        return data


class GameResult(Schema):

    narrations = fields.List(fields.String(), required=True)

    @post_load
    def make_results(self, data, **kwargs):
        return '\n'.join(
            data['narrations']
        )


if __name__ == "__main__":
    schema = GameSchema()
    data = {
        "player1": {
            "name": "Tony",
            "moves": ["D", "DSD"],
            "strikes": ["K", "P", "K"]
        },
        "player2": {
            "name": "Arnoldo",
            "moves": ["D", "DSD"],
            "strikes": ["K", "P", "K"]
        },
    }

    des_data = GameSchema().load(data)
    print(
        des_data
    )