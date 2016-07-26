$(document).ready(function() {
	ws = new WebSocket('ws://' + location.hostname + ':' + location.port + location.pathname + '/websocket');

	ws.onopen = function() {
    send_print(ws, "Opened WebSocket");
    send_create_board(ws, window.num_rows, window.num_columns, window.num_to_win);
    send_add_player(ws, "Alice", "black");
    send_add_player(ws, "Bob", "red");
    send_start_game(ws);
	};

	ws.onmessage = function(e) {
    console.log(e.data);
	};

});


function send_print(ws, message) {
  ws.send(JSON.stringify({
    "kind": "print",
    "message": message,
  }));
}


function send_add_player(ws, name, color) {
  ws.send(JSON.stringify({
    "kind": "add_player",
    "name": name,
    "color": color,
  }));
}


function send_create_board(ws, num_rows, num_columns, num_to_win) {
  ws.send(JSON.stringify({
    "kind": "create_board",
    "num_rows": num_rows,
    "num_columns": num_columns,
    "num_to_win": num_to_win,
  }));
}


function send_start_game(ws) {
  ws.send(JSON.stringify({
    "kind": "start_game",
  }));
}


function send_play(ws, column) {
  ws.send(JSON.stringify({
    "kind": "play",
    "column": column,
  }));
}
