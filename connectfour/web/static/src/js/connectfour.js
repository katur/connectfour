import wsClient from 'socket.io-client';
import React from 'react';
import ReactDOM from 'react-dom';
import { createStore } from 'redux';
import { Provider } from 'react-redux';

import App from './components/App';
import appReducer from './reducers';
import {
  setIDs, setRoomDoesNotExist, updatePlayers, updatePlayer, addPlayer,
  removePlayer, setNextPlayer, updateBoard, resetBoard, colorSquare,
  blinkSquares, unblinkSquares, startGame, stopGame, reportDraw,
  reportTryAgain,
} from './actions';

// This is where webpack compiles my sass to css
import '../stylesheets/styles';


//////////////////////////
// Connect to WebSocket //
//////////////////////////

const WS_URL = `${location.protocol}//${document.domain}:${location.port}`;
window.ws = wsClient(WS_URL);


/////////////////////////////////////////////
// Create Redux store and render React app //
/////////////////////////////////////////////

const store = createStore(appReducer);

ReactDOM.render(
  <Provider store={store}>
    <App />
  </Provider>,
  document.getElementById('react-root')
);


/////////////////////////////////////////////////////////////////
// Respond to WebSocket events (these mostly update the store) //
/////////////////////////////////////////////////////////////////

window.ws.on('roomJoined', (data) => {
  store.dispatch(setIDs(data.pk, data.room));

  if (data.board) {
    store.dispatch(updateBoard(data.board));
  }

  if (data.players) {
    store.dispatch(updatePlayers(data.players));
  }
});

window.ws.on('roomDoesNotExist', () => {
  store.dispatch(setRoomDoesNotExist())
});

window.ws.on('playerAdded', ({ player }) => {
  store.dispatch(addPlayer(player))
});

window.ws.on('playerRemoved', ({ player }) => {
  store.dispatch(removePlayer(player))
});

window.ws.on('nextPlayer', ({ player }) => {
  store.dispatch(setNextPlayer(player))
});

window.ws.on('boardCreated', ({ board }) => {
  store.dispatch(unblinkSquares());
  store.dispatch(updateBoard(board));
});

window.ws.on('colorPlayed', ({ color, position }) => {
  store.dispatch(colorSquare(color, position));
});

window.ws.on('gameStarted', () => {
  store.dispatch(unblinkSquares());
  store.dispatch(resetBoard());
  store.dispatch(startGame());
});

window.ws.on('gameWon', ({ winner, winningPositions, players }) => {
  store.dispatch(stopGame());
  store.dispatch(blinkSquares(winningPositions));
  store.dispatch(updatePlayers(players));
});

window.ws.on('gameDraw', ({ players }) => {
  store.dispatch(stopGame());
  store.dispatch(updatePlayers(players));
  store.dispatch(reportDraw());
});

window.ws.on('tryAgain', ({ player, reason }) => {
  store.dispatch(reportTryAgain(player, reason));
});
