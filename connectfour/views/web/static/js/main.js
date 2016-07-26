$(document).ready(function() {
	window.ws = new WebSocket('ws://' + location.hostname + ':' +
                            location.port + location.pathname + '/ws');

	window.ws.onopen = function() {
    sendPrint("Opened WebSocket");
    setupGame();
	};

	window.ws.onmessage = function(e) {
    console.log(e.data);
	};

});


function setupGame() {
  sendCreateBoard(num_rows, num_columns, num_to_win);
  for (var i = 0; i < players.length; i++) {
    sendAddPlayer(players[i], colors[i]);
  }
  sendStartGame();
}


function sendAddPlayer(name, color) {
  window.ws.send(JSON.stringify({
    "kind": "add_player",
    "name": name,
    "color": color,
  }));
}


function sendCreateBoard(num_rows, num_columns, num_to_win) {
  window.ws.send(JSON.stringify({
    "kind": "create_board",
    "num_rows": num_rows,
    "num_columns": num_columns,
    "num_to_win": num_to_win,
  }));
}


function sendStartGame() {
  window.ws.send(JSON.stringify({
    "kind": "start_game",
  }));
}


function sendPlay(column) {
  window.ws.send(JSON.stringify({
    "kind": "play",
    "column": column,
  }));
}


function sendPrint(message) {
  window.ws.send(JSON.stringify({
    "kind": "print",
    "message": message,
  }));
}
