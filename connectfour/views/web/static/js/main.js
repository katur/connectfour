$(document).ready(function() {
	ws = new WebSocket('ws://' + location.hostname + ':' + location.port + location.pathname + '/websocket');

	ws.onopen = function() {
		ws.send("Opened WebSocket");
	};

	ws.onmessage = function(e) {
    console.log(e.data);
	};
});
