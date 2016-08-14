/*
 * action types
 */
export const SET_USERNAME = "SET_USERNAME";
export const SET_ROOM = "SET_ROOM";
export const ADD_PLAYER = "ADD_PLAYER";
export const REMOVE_PLAYER = "REMOVE_PLAYER";
export const SET_CURRENT_PLAYER_INDEX = "SET_CURRENT_PLAYER_INDEX";


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

export function removePlayer(player) {
  return {
    type: REMOVE_PLAYER,
    player
  }
}

export function setCurrentPlayerIndex(index) {
  return {
    type: SET_CURRENT_PLAYER_INDEX,
    index
  }
}
