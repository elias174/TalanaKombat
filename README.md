# Talana Kombat

A simple game that confronts 2 characters, _Tony_ and _Arnoldo_.

## Dependencies

To run the Rest API it's necessary install the requirements with:

```
pip install -r requirements.txt
```


## The Game

The game have the next rules:

-   Each player starts with 6 energy points.
-   Each player has 2 movements combo (with 2 and 3 points of damage), and simple strikes (with 1 point of damage for each one).
-   Each player submits two `lists` of `strings`, one for the moves and one for the strikes.
-   The game is played in turns, the game decides which player starts (The decision is based on the length of the moves, in case of equality, the first player will start).
-   The game ends when the energy of a player is less than 1.
-   A move string is composed by the characters of `W`, `A`, `S` or `D` (it's possible to combine one or more). A strike string is composed by `P` or `K` characters.

## Usage

You can play the game with the CLI game_engine module or with the API REST.

### CLI

To play the game, you need send to the game_engine module two PlayerInfo objects, and initialize the objects with a List of Strings of moves and strikes, and a dictionary object with the combos.

```python
    from game_engine import MovementCombo
    from game_engine import GameEngine
    from game_engine import PlayerInfo
    
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
```


The method `game.get_narration_of_game()` method returns a narration for the battle performed, this narration consists in a `list` of `Strings`.

```shell

[
  'Tony avanza, Tony le da una patada al pobre Arnoldo', 
  'Arnoldo conecta un Remuyuken', 
  'Tony conecta un Taladoken', 
  'Arnoldo se agacha',
  'Arnoldo avanza', 
  'Tony se agacha', 
  'Arnoldo conecta un Remuyuken', 
  'Arnoldo gana y aun le queda 2 de energia'
]


```

## REST API

### Local VirtualEnvironment

After install the requirements, just run the script `./run_local.sh`

### Docker Environment

A Dockerfile is on the repository you can build an image or use the image generated in DockerHub with the commands:

```
docker pull elias174/talanakombat
```

Run the docker image

```
docker run -it -p 5000:5000 -d elias174/talanakombat
```


### Sending Data to the API

And send a request to the following URL (assuming you have flask running on port 5000):

```
POST 127.0.0.1:5000/game
```

With a JSON with a structure like this:

```json
{
    "player1": {
      "name": "Tony",
      "moves": ["D", "DSD", "S", "DSD", "SD"],
      "strikes": ["K", "P", "", "K", "P"]
    },
    "player2": {
      "name": "Arnoldo",
      "moves": ["SA", "SA", "SA", "ASA", "SA"],
      "strikes": ["K", "", "K", "P", "P"]
    }
}
```
