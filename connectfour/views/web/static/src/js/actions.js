/*
 * action types
 */
export const SET_LOGGED_IN_USER = "SET_LOGGED_IN_USER";
export const INITIALIZE_BOARD = "INITIALIZE_BOARD";
export const INITIALIZE_PLAYERS = "INITIALIZE_PLAYERS";
export const ADD_PLAYER = "ADD_PLAYER";
export const REMOVE_PLAYER = "REMOVE_PLAYER";
export const START_GAME = "START_GAME";
export const SET_NEXT_PLAYER = "SET_NEXT_PLAYER";
export const COLOR_SQUARE = "COLOR_SQUARE";
export const TRY_AGAIN = "TRY_AGAIN";
export const GAME_WON = "GAME_WON";
export const GAME_DRAW = "GAME_DRAW";


/*
 * action creators
 */

export function setLoggedInUser(pk, username, room) {
  return {
    type: SET_LOGGED_IN_USER,
    pk,
    username,
    room,
  }
}

export function initializeBoard(board) {
  return {
    type: INITIALIZE_BOARD,
    board,
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

export function removePlayer(player) {
  return {
    type: REMOVE_PLAYER,
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

export function tryAgain(player, reason) {
  return {
    type: TRY_AGAIN,
    player,
    reason,
  }
}

export function gameWon(player) {
  return {
    type: GAME_WON,
    player,
  }
}

export function gameDraw() {
  return {
    type: GAME_DRAW,
  }
}
