const Emitters = {
  addFirstPlayer: function({ username }) {
    window.ws.emit("add_first_player", {
      "username": username,
    });
  },

  addPlayer: function ({ username, room }) {
    window.ws.emit("add_player", {
      "username": username,
      "room": room,
    });
  },

  createBoard: function({ numRows, numColumns, numToWin }) {
    window.ws.emit("create_board", {
      "num_rows": numRows,
      "num_columns": numColumns,
      "num_to_win": numToWin,
    });
  },

  startGame: function() {
    window.ws.emit("start_game", {});
  },

  play: function({ column }) {
    window.ws.emit("play", {
      "column": column,
    });
  },

  print: function({ message }) {
    window.ws.emit("print", {
      "message": message,
    });
  },
};


export default Emitters;
