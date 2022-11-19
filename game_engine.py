import itertools

from typing import Tuple


class MovementCombo(object):
    def __init__(self, move, strike, damage, narration):
        self.move = move
        self.strike = strike
        self.damage = damage
        self.narration = narration

    def __str__(self):
        return f"{self.move}{self.strike} -> {self.narration}"


class PlayerInfo(object):

    GENERAL_MOVEMENTS = {
        'P': MovementCombo('', 'P', 1, '{player_name} le da un puñetazo al pobre {opponent}'),
        'K': MovementCombo('', 'K', 1, '{player_name} le da una patada al pobre {opponent}'),
        'A': MovementCombo('A', '', 0, '{player_name} avanza'),
        'D': MovementCombo('D', '', 0, '{player_name} avanza'),
        'W': MovementCombo('W', '', 0, '{player_name} salta'),
        'S': MovementCombo('S', '', 0, '{player_name} se agacha'),
    }

    def __init__(self, moves: list, strikes: list, name: str, damage_combos: dict):
        self.moves = moves
        self.strikes = strikes
        self.name = name
        self.energy = 6
        self.combos_mapping_movements = damage_combos

    def reduce_energy(self, damage):
        self.energy -= damage

    def is_dead(self):
        return self.energy < 1

    def __str__(self):
        return self.name

    def get_narration_damage_combo_from_data(self, move, strike, opponent_name) -> Tuple[str, int]:
        move_and_combos = []
        combo_finded = None
        residual_moves = ''
        for index, char_move in enumerate(move):
            combo_finded = self.combos_mapping_movements.get(f"{move[index:]}{strike}")
            residual_moves = move[:index]
            if combo_finded:
                break

        if not combo_finded:
            residual_moves = move

        for char_move in residual_moves:
            simple_movement = self.GENERAL_MOVEMENTS.get(char_move)
            if simple_movement:
                move_and_combos.append(simple_movement)

        if combo_finded:
            move_and_combos.append(combo_finded)
        elif self.GENERAL_MOVEMENTS.get(strike):
            move_and_combos.append(self.GENERAL_MOVEMENTS.get(strike))

        composed_narration = [combo_move.narration for combo_move in move_and_combos]
        composed_narration = ', '.join(composed_narration)
        composed_damage = sum(combo_move.damage for combo_move in move_and_combos)

        return composed_narration.format(player_name=self.name, opponent=opponent_name), composed_damage

    @property
    def count_moves(self):
        return len(self.moves)

    @property
    def count_strikes(self):
        return len(self.strikes)

    @property
    def count_total(self):
        return len(self.strikes) + len(self.moves)


class GameEngine(object):

    @staticmethod
    def who_starts(player_info_j1: PlayerInfo, player_info_j2: PlayerInfo):
        if player_info_j1.count_total < player_info_j2.count_total:
            return player_info_j1, player_info_j2
        elif player_info_j1.count_total < player_info_j1.count_total:
            return player_info_j2, player_info_j1
        elif player_info_j1.count_moves < player_info_j2.count_moves:
            return player_info_j1, player_info_j2
        elif player_info_j2.count_moves < player_info_j1.count_moves:
            return player_info_j2, player_info_j1
        elif player_info_j1.count_strikes < player_info_j2.count_strikes:
            return player_info_j1, player_info_j2
        elif player_info_j2.count_strikes < player_info_j1.count_strikes:
            return player_info_j2, player_info_j1
        else:
            return player_info_j1, player_info_j2

    def __init__(self, player_info_j1: PlayerInfo, player_info_j2: PlayerInfo):
        self.start_player, self.second_player = self.who_starts(player_info_j1, player_info_j2)

    def get_narration_of_game(self):
        iterable_start_player = itertools.zip_longest(
            self.start_player.moves, self.start_player.strikes, fillvalue='')
        iterable_second_player = itertools.zip_longest(
            self.second_player.moves, self.second_player.strikes, fillvalue='')

        narrations = []
        for combo_start_player, combo_second_player in itertools.zip_longest(
                iterable_start_player, iterable_second_player, fillvalue=('', '')):

            narration_start_player, damage_start_player = self.start_player.get_narration_damage_combo_from_data(
                combo_start_player[0], combo_start_player[1], self.second_player.name)

            if narration_start_player:
                narrations.append(narration_start_player)
            self.second_player.reduce_energy(damage_start_player)
            if self.second_player.is_dead():
                narrations.append(f"{self.start_player.name} gana y aun le queda "
                                  f"{self.start_player.energy} de energia")
                return narrations

            narration_second_player, damage_second_player = self.second_player.get_narration_damage_combo_from_data(
                combo_second_player[0], combo_second_player[1], self.start_player.name)

            if narration_second_player:
                narrations.append(narration_second_player)
            self.start_player.reduce_energy(damage_second_player)
            if self.start_player.is_dead():
                narrations.append(f"{self.second_player.name} gana y aun le queda"
                                  f" {self.second_player.energy} de energia")
                return narrations

        return narrations


if __name__ == "__main__":
    moves_j1 = ["D", "DSD", "S", "DSD", "SD"]
    strikes_j1 = ["K", "P", "", "K", "P"]
    movements_combo_j1 = {
        'DSDP': MovementCombo('DSD', 'P', 3, '{player_name} conecta un Taladoken'),
        'SDK': MovementCombo('SD', 'K', 2, '{player_name} conecta un Remuyuken')
    }
    j1 = PlayerInfo(moves_j1, strikes_j1, 'Tony', movements_combo_j1)

    moves_j2 = ["SA", "SA", "SA", "ASA", "SA"]
    strikes_j2 = ["K", "", "K", "P", "P"]
    movements_combo_j2 = {
        'SAK': MovementCombo('SA', 'K', 3, '{player_name} conecta un Remuyuken'),
        'ASAP': MovementCombo('ASA', 'P', 2, '{player_name} conecta un Taladoken')
    }
    j2 = PlayerInfo(moves_j2, strikes_j2, 'Arnoldo', movements_combo_j2)

    game = GameEngine(j1, j2)
    print(*game.get_narration_of_game(), sep='\n')
