const Emitters = {
  addUser: function ({ username, room }) {
    window.ws.emit("addUser", {
      "username": username,
      "room": room,
    });
  },

  createBoard: function({ numRows, numColumns, numToWin }) {
    window.ws.emit("createBoard", {
      "numRows": numRows,
      "numColumns": numColumns,
      "numToWin": numToWin,
    });
  },

  startGame: function() {
    window.ws.emit("startGame", {});
  },

  play: function({ column }) {
    window.ws.emit("play", {
      "column": column,
    });
  },
};


export default Emitters;
