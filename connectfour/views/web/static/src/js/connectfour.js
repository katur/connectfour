import React from "react";
import ReactDOM from "react-dom";
import App from "./components/App";
import { createStore } from "redux";
import { Provider } from 'react-redux';
import appReducer from "./reducers";
import { setUsername, setRoom, addPlayer } from "./actions";
import "../stylesheets/connectfour";
import $ from "jquery";
import wsClient from "socket.io-client";


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
});

window.ws.on("player_added", function(data) {
  store.dispatch(addPlayer(data.player));
});

window.ws.on("board_created", function(data) {
  updateFeedbackBar("Board created");
  drawBoard(data.num_rows, data.num_columns, data.num_to_win);
});

window.ws.on("game_started", function(data) {
  resetBoard();
  disablePlayAgainButton();
  enablePlayButtons();
  updateGameNumber(data.game_number);
});

window.ws.on("next_player", function(data) {
  updateFeedbackBar(data.player + "'s turn");
});

window.ws.on("color_played", function(data) {
  updateGameSquare(data.color, data.position);
});

window.ws.on("try_again", function(data) {
  updateFeedbackBar(data.player + " try again (" + data.reason + ")");
});

window.ws.on("game_won", function(data) {
  disablePlayButtons();
  updateFeedbackBar("Game won by " + data.player);
  enablePlayAgainButton()
});

window.ws.on("game_draw", function(data) {
  disablePlayButtons();
  updateFeedbackBar("Game ended in a draw");
  enablePlayAgainButton()
});

window.ws.on("message", function(message) {
  console.log(message);
});


///////////////////////////////////////////////////////////////
// Helpers that i'll mostly be migrating to React components //
///////////////////////////////////////////////////////////////

function drawBoard(numRows, numColumns, numToWin) {
  var percentage = 80.0 / Math.max(numRows, numColumns);

  var columnButtons = $("#column-buttons");
  var buttonStyle = "width:" + percentage + "vmin;";
  for (var i = 0; i < numColumns; i++) {
    columnButtons.append(
      "<button class='column-play' style='" + buttonStyle +
      "' onclick='sendPlay(" + i + ")' disabled>Play here</button>");
  }

  var gameGrid = $("#game-grid");
  for (var i = 0; i < numRows; i++) {
    for (var j = 0; j < numColumns; j++) {
      var squareStyle = "width:" + percentage + "vmin; " +
                        "height:" + percentage + "vmin; ";
      if (j === 0) {
        squareStyle += "clear: left; ";
      }
      gameGrid.append("<div id='square-" + i + "-" + j +
                      "' class='game-square' style='" + squareStyle +
                      "'></div>");
    }
  }

  resetBoard();
}

function drawPlayAgain() {
  $("#more-controls").append(
    "<button id='play-again' onclick='sendStartGame();'>Play again?</button>");
}

function resetBoard() {
  $(".game-square").css("background", "#fcef03");
}

function updateGameTitle(room) {
  $("#game-title").text("Game Room " + room);
}

function updateGameSquare(color, position) {
  id = "#square-" + position[0] + "-" + position[1];
  $(id).css("background", color);
}

function updateFeedbackBar(message) {
  $("#game-feedback").text(message);
}

function updateGameNumber(number) {
  $("#game-number").text(number);
}

function enablePlayButtons() {
  $(".column-play").removeAttr("disabled");
}

function disablePlayButtons() {
  $(".column-play").attr("disabled", true);
}

function enablePlayAgainButton() {
  $("#play-again").removeAttr("disabled");
}

function disablePlayAgainButton() {
  $("#play-again").attr("disabled", true);
}
