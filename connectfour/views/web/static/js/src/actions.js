/*
 * action types
 */

export const SET_IDS = "SET_IDS";
export const SET_ROOM_DOES_NOT_EXIST = "SET_ROOM_DOES_NOT_EXIST";
export const SET_PLAYERS = "SET_PLAYERS";
export const ADD_PLAYER = "ADD_PLAYER";
export const REMOVE_PLAYER = "REMOVE_PLAYER";
export const SET_NEXT_PLAYER = "SET_NEXT_PLAYER";
export const SET_BOARD = "SET_BOARD";
export const START_GAME = "START_GAME";
export const COLOR_SQUARE = "COLOR_SQUARE";
export const TRY_AGAIN = "TRY_AGAIN";
export const GAME_WON = "GAME_WON";
export const GAME_DRAW = "GAME_DRAW";


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

export function startGame(gameNumber) {
  return {
    type: START_GAME,
    gameNumber,
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

export function gameWon(player, winningPositions) {
  return {
    type: GAME_WON,
    player,
    winningPositions,
  }
}

export function gameDraw() {
  return {
    type: GAME_DRAW,
  }
}
