import React from "react";
import ReactDOM from "react-dom";
import App from "./components/App.jsx";
import "../stylesheets/connectfour.sass";
import $ from "jquery";
import wsClient from "socket.io-client";

const WS_URL = "http://" + document.domain + ":" + location.port;


window.ws = wsClient(WS_URL);


$(document).ready(function() {

  ReactDOM.render(<App />, document.getElementById("react-root"));

  /////////////////////////
  // Process setup forms //
  /////////////////////////

  $("#new-game-form").submit(function(e) {
    console.log("submitted new game form");
    e.preventDefault();
    processNewGameForm();
  });

  $("#join-game-form").submit(function(e) {
    console.log("submitted join game form");
    e.preventDefault();
    processJoinGameForm();
  });

  //////////////////////////////
  // Respond to server events //
  //////////////////////////////

  window.ws.on("message", function(message) {
    console.log(message);
  });

  window.ws.on("board_created", function(data) {
    updateFeedbackBar("Board created");
    drawBoard(data.num_rows, data.num_columns, data.num_to_win);
  });

  window.ws.on("player_added", function(data) {
    updateFeedbackBar("Welcome, " + data.player);
    updateGameTitle(data.room);
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
});


function sendCreateBoard(numRows, numColumns, numToWin) {
  window.ws.emit("create_board", {
    "num_rows": numRows,
    "num_columns": numColumns,
    "num_to_win": numToWin,
  });
}


function sendAddFirstPlayer(username) {
  window.ws.emit("add_first_player", {
    "username": username,
  });
}


function sendAddPlayer(username, room) {
  window.ws.emit("add_player", {
    "username": username,
    "room": room,
  });
}


function sendStartGame() {
  window.ws.emit("start_game", {});
}


function sendPlay(column) {
  window.ws.emit("play", {
    "column": column,
  });
}


function sendPrint(message) {
  window.ws.emit("print", {
    "message": message,
  });
}


function processNewGameForm() {
  console.log("processing new game form");
  var username = $("input[name=first-username]").val();
  sendAddFirstPlayer(username);

  var numRows = $("input[name=num-rows]").val();
  var numColumns = $("input[name=num-columns]").val();
  var numToWin = $("input[name=num-to-win]").val();
  sendCreateBoard(numRows, numColumns, numToWin);

  $("#setup-content").hide();
  $("#game-content").show();
}


function processJoinGameForm() {
  console.log("processing join game form");
  var username = $("input[name=join-username]").val();
  var room = $("input[name=room]").val();
  sendAddPlayer(username, room);

  $("#setup-content").hide();
  $("#game-content").show();
}


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
