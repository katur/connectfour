import wsClient from "socket.io-client";
import "../stylesheets/connectfour";
import React from "react";
import ReactDOM from "react-dom";
import App from "./components/App";
import { createStore } from "redux";
import { Provider } from 'react-redux';
import appReducer from "./reducers";
import {
  setUsername, setRoom, initializeBoard, initializePlayers, addPlayer,
  startGame, setNextPlayer, colorSquare, tryAgain, gameWon, gameDraw,
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


//////////////////////////////////////////////////////////////////////
// Respond to WebSocket events (these will mostly update the store) //
//////////////////////////////////////////////////////////////////////

window.ws.on("roomJoined", function(data) {
  store.dispatch(setUsername(data.username));
  store.dispatch(setRoom(data.room));

  if (data.board) {
    store.dispatch(initializeBoard(data.board));
  }

  if (data.players) {
    store.dispatch(initializePlayers(data.players));
  }
});

window.ws.on("boardCreated", function(data) {
  store.dispatch(initializeBoard(data.board));
});

window.ws.on("playerAdded", function(data) {
  store.dispatch(addPlayer(data.player));
});

window.ws.on("gameStarted", function(data) {
  store.dispatch(initializeBoard(data.board));
  store.dispatch(startGame(data.gameNumber));
});

window.ws.on("nextPlayer", function(data) {
  store.dispatch(setNextPlayer(data.player));
});

window.ws.on("colorPlayed", function(data) {
  store.dispatch(colorSquare(data.color, data.position));
});

window.ws.on("tryAgain", function(data) {
  store.dispatch(tryAgain(data.player, data.reason));
});

window.ws.on("gameWon", function(data) {
  store.dispatch(gameWon(data.player));
});

window.ws.on("gameDraw", function(data) {
  store.dispatch(gameDraw());
});

window.ws.on("message", function(message) {
  console.log(message);
});
