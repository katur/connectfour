import wsClient from "socket.io-client";
import "../../stylesheets/src/styles";
import React from "react";
import ReactDOM from "react-dom";
import App from "./components/App";
import { createStore } from "redux";
import { Provider } from 'react-redux';
import appReducer from "./reducers";
import {
  setIDs, setRoomDoesNotExist,
  setPlayers, setNextPlayer, addPlayer, removePlayer, updatePlayer,
  setBoard, resetBoard, colorSquare, blinkSquares, unblinkSquares,
  startGame, stopGame, reportDraw, reportTryAgain,
} from "./actions";


/////////////////////////////////////////////
// Create Redux store and render React app //
/////////////////////////////////////////////

let store = createStore(appReducer);

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


/////////////////////////////////////////////////////////////////
// Respond to WebSocket events (these mostly update the store) //
/////////////////////////////////////////////////////////////////

window.ws.on("roomJoined", function(data) {
  store.dispatch(setIDs(data.pk, data.room));

  if (data.board) {
    store.dispatch(setBoard(data.board));
  }

  if (data.players) {
    store.dispatch(setPlayers(data.players));
  }
});

window.ws.on("roomDoesNotExist", function() {
  store.dispatch(setRoomDoesNotExist());
});

window.ws.on("nextPlayer", function(data) {
  store.dispatch(setNextPlayer(data.player));
});

window.ws.on("playerAdded", function(data) {
  store.dispatch(addPlayer(data.player));
});

window.ws.on("playerRemoved", function(data) {
  store.dispatch(removePlayer(data.player));
});

window.ws.on("boardCreated", function(data) {
  store.dispatch(unblinkSquares());
  store.dispatch(setBoard(data.board));
});

window.ws.on("colorPlayed", function(data) {
  store.dispatch(colorSquare(data.color, data.position));
});

window.ws.on("gameStarted", function(data) {
  store.dispatch(unblinkSquares());
  store.dispatch(resetBoard());
  store.dispatch(startGame(data.gameNumber));
});

window.ws.on("gameWon", function(data) {
  store.dispatch(stopGame());
  store.dispatch(setPlayers(data.players));
  store.dispatch(blinkSquares(data.winningPositions));
  store.dispatch(updatePlayer(data.winner));
});

window.ws.on("gameDraw", function(data) {
  store.dispatch(stopGame());
  store.dispatch(setPlayers(data.players));
  store.dispatch(reportDraw());
});

window.ws.on("tryAgain", function(data) {
  store.dispatch(reportTryAgain(data.player, data.reason));
});

window.ws.on("message", function(message) {
  console.log(message);
});
