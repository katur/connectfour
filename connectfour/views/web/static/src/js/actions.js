/*
 * action types
 */
export const SET_USERNAME = "SET_USERNAME";
export const SET_ROOM = "SET_ROOM";
export const INITIALIZE_BOARD = "INITIALIZE_BOARD";
export const INITIALIZE_PLAYERS = "INITIALIZE_PLAYERS";
export const ADD_PLAYER = "ADD_PLAYER";
export const START_GAME = "START_GAME";
export const SET_NEXT_PLAYER = "SET_NEXT_PLAYER";
export const COLOR_SQUARE = "COLOR_SQUARE";


/*
 * action creators
 */
export function setUsername(username) {
  return {
    type: SET_USERNAME,
    username
  }
}

export function setRoom(room) {
  return {
    type: SET_ROOM,
    room
  }
}

export function initializeBoard(board) {
  return {
    type: INITIALIZE_BOARD,
    board
  }
}

export function initializePlayers(players) {
  return {
    type: INITIALIZE_PLAYERS,
    players,
  }
}

export function addPlayer(player) {
  return {
    type: ADD_PLAYER,
    player,
  }
}

export function startGame(gameNumber) {
  return {
    type: START_GAME,
    gameNumber,
  }
}

export function setNextPlayer(player) {
  return {
    type: SET_NEXT_PLAYER,
    player,
  }
}

export function colorSquare(color, position) {
  return {
    type: COLOR_SQUARE,
    color,
    position,
  }
}
