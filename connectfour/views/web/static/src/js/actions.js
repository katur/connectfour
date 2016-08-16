/*
 * action types
 */
export const SET_USERNAME = "SET_USERNAME";
export const SET_ROOM = "SET_ROOM";
export const ADD_PLAYER = "ADD_PLAYER";
export const CREATE_BOARD = "CREATE_BOARD";
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

export function addPlayer(player) {
  return {
    type: ADD_PLAYER,
    player
  }
}

export function createBoard(board) {
  return {
    type: CREATE_BOARD,
    board
  }
}

export function setCurrentPlayer(player) {
  return {
    type: SET_CURRENT_PLAYER,
    player
  }
}
