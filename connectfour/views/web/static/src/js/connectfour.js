import wsClient from "socket.io-client";
import $ from "jquery";
import "../stylesheets/connectfour";
import React from "react";
import ReactDOM from "react-dom";
import App from "./components/App";
import { createStore } from "redux";
import { Provider } from 'react-redux';
import appReducer from "./reducers";
import {
  setUsername,
  setRoom,
  initializeBoard,
  initializePlayers,
  addPlayer,
  startGame,
  setNextPlayer,
  colorSquare,
} from "./actions";


/////////////////////////////////////////////
// Create Redux store and render React app //
/////////////////////////////////////////////

let store = createStore(appReducer);
// let store = createStore(appReducer, window.STATE_FROM_SERVER);

ReactDOM.render(
  <Provider store={store}>
    <App />
  </Provider>,
  document.getElementById("react-root")
);


//////////////////////////
// Connect to WebSocket //
//////////////////////////

const WS_URL = "http://" + document.domain + ":" + location.port;
window.ws = wsClient(WS_URL);


//////////////////////////////////////////////////////////////////////
// Respond to WebSocket events (these will mostly update the store) //
//////////////////////////////////////////////////////////////////////

window.ws.on("room_joined", function(data) {
  store.dispatch(setUsername(data.username));
  store.dispatch(setRoom(data.room));

  if (data.board) {
    store.dispatch(initializeBoard(data.board));
  }

  if (data.players) {
    store.dispatch(initializePlayers(data.players));
  }
});

window.ws.on("board_created", function(data) {
  store.dispatch(initializeBoard(data.board));
});

window.ws.on("player_added", function(data) {
  store.dispatch(addPlayer(data.player));
});

window.ws.on("game_started", function(data) {
  store.dispatch(startGame(data.game_number));
});

window.ws.on("next_player", function(data) {
  store.dispatch(setNextPlayer(data.player));
});

window.ws.on("color_played", function(data) {
  store.dispatch(colorSquare(data.color, data.position));
});

window.ws.on("try_again", function(data) {
  // updateFeedbackBar(data.player.name + " try again (" + data.reason + ")");
});

window.ws.on("game_won", function(data) {
  // disablePlayButtons();
  // updateFeedbackBar("Game won by " + data.player.name);
  // enablePlayAgainButton()
});

window.ws.on("game_draw", function(data) {
  // disablePlayButtons();
  // updateFeedbackBar("Game ended in a draw");
  // enablePlayAgainButton()
});

window.ws.on("message", function(message) {
  console.log(message);
});


///////////////////////////////////////////////////////////////
// Helpers that i'll mostly be migrating to React components //
///////////////////////////////////////////////////////////////

function updateGameSquare(color, position) {
  id = "#square-" + position[0] + "-" + position[1];
  $(id).css("background", color);
}

function updateFeedbackBar(message) {
  $("#game-feedback").text(message);
}

function disablePlayButtons() {
  $(".column-play").attr("disabled", true);
}

function enablePlayAgainButton() {
  $("#play-again").removeAttr("disabled");
}
