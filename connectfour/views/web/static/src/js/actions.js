/*
 * action types
 */
export const SET_USERNAME = "SET_USERNAME";
export const SET_ROOM = "SET_ROOM";
export const INITIALIZE_BOARD = "INITIALIZE_BOARD";
export const INITIALIZE_PLAYERS = "INITIALIZE_PLAYERS";
export const ADD_PLAYER = "ADD_PLAYER";
export const SET_CURRENT_PLAYER = "SET_CURRENT_PLAYER";


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
    players
  }
}

export function addPlayer(player) {
  return {
    type: ADD_PLAYER,
    player
  }
}

export function setCurrentPlayer(player) {
  return {
    type: SET_CURRENT_PLAYER,
    player
  }
}
