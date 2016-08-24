/*
 * action types
 */

export const SET_IDS = "SET_IDS";
export const SET_ROOM_DOES_NOT_EXIST = "SET_ROOM_DOES_NOT_EXIST";

export const SET_PLAYERS = "SET_PLAYERS";
export const ADD_PLAYER = "ADD_PLAYER";
export const REMOVE_PLAYER = "REMOVE_PLAYER";
export const UPDATE_PLAYER = "UPDATE_PLAYER";
export const SET_NEXT_PLAYER = "SET_NEXT_PLAYER";

export const SET_BOARD = "SET_BOARD";
export const RESET_BOARD = "RESET_BOARD";
export const COLOR_SQUARE = "COLOR_SQUARE";
export const BLINK_SQUARES = "BLINK_SQUARES";
export const UNBLINK_SQUARES = "UNBLINK_SQUARES";

export const START_GAME = "START_GAME";
export const STOP_GAME = "STOP_GAME";
export const REPORT_DRAW = "REPORT_DRAW";
export const REPORT_TRY_AGAIN = "REPORT_TRY_AGAIN";


/*
 * action creators
 */

export function setIDs(pk, room) {
  return {
    type: SET_IDS,
    pk,
    room,
  }
}

export function setRoomDoesNotExist() {
  return {
    type: SET_ROOM_DOES_NOT_EXIST,
  }
}

export function setPlayers(players) {
  return {
    type: SET_PLAYERS,
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

export function updatePlayer(player) {
  return {
    type: UPDATE_PLAYER,
    player,
  }
}

export function setNextPlayer(player) {
  return {
    type: SET_NEXT_PLAYER,
    player,
  }
}

export function setBoard(board) {
  return {
    type: SET_BOARD,
    board,
  }
}

export function resetBoard() {
  return {
    type: RESET_BOARD,
  }
}

export function colorSquare(color, position) {
  return {
    type: COLOR_SQUARE,
    color,
    position,
  }
}

export function blinkSquares(positions) {
  return {
    type: BLINK_SQUARES,
    positions,
  }
}

export function unblinkSquares() {
  return {
    type: UNBLINK_SQUARES,
  }
}

export function startGame() {
  return {
    type: START_GAME,
  }
}

export function stopGame() {
  return {
    type: STOP_GAME,
  }
}

export function reportDraw() {
  return {
    type: REPORT_DRAW,
  }
}

export function reportTryAgain(player, reason) {
  return {
    type: REPORT_TRY_AGAIN,
    player,
    reason,
  }
}
