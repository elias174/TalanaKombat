curl -X POST -H "Content-Type: application/json" -d '{
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
}' https://1jvx90ljsj.execute-api.us-west-2.amazonaws.com/dev/game