import {
  SET_IDS, SET_ROOM_DOES_NOT_EXIST,
  UPDATE_PLAYERS, UPDATE_PLAYER, ADD_PLAYER, REMOVE_PLAYER, SET_NEXT_PLAYER,
  UPDATE_BOARD, RESET_BOARD, COLOR_SQUARE, BLINK_SQUARES, UNBLINK_SQUARES,
  START_GAME, STOP_GAME, REPORT_DRAW, REPORT_TRY_AGAIN,
} from "./actions";


const initialState = {
  pk: ``,
  room: ``,
  roomDoesNotExist: false,

  gameInProgress: false,
  feedback: ``,

  grid: [[]],
  blinkingSquares: [],
  numRows: null,
  numColumns: null,
  numToWin: null,

  players: [],
  nextPlayer: null,
}


function update(state, mutations) {
  return Object.assign({}, state, mutations);
}


function appReducer(state = initialState, action) {
  switch(action.type) {

    case SET_IDS:
      return update(state, {
        pk: action.pk,
        room: action.room,
      });

    case SET_ROOM_DOES_NOT_EXIST:
      return update(state, {
        roomDoesNotExist: true,
      });

    case UPDATE_PLAYERS:
      return update(state, {
        players: action.players,
      });

    case UPDATE_PLAYER:
      var newPlayers = state.players.map(function(player) {
        return (player.pk === action.player.pk) ? action.player : player;
      });

      return update(state, {
        players: newPlayers,
      })

    case ADD_PLAYER:
      return update(state, {
        players: [
          ...state.players,
          action.player,
        ],
      });

    case REMOVE_PLAYER:
      var newPlayers = state.players.filter(function(player) {
        return player.pk !== action.player.pk;
      });

      return update(state, {
        players: newPlayers,
      });

    case SET_NEXT_PLAYER:
      return update(state, {
        nextPlayer: action.player,
      });

    case UPDATE_BOARD:
      return update(state, {
        numRows: action.board.numRows,
        numColumns: action.board.numColumns,
        numToWin: action.board.numToWin,
        grid: action.board.grid,
      });

    case RESET_BOARD:
      var newGrid = state.grid.map(function(row) {
        return row.map(function(column) {
          return null;
        });
      });

      return update(state, {
        grid: newGrid,
      });

    case COLOR_SQUARE:
      var newGrid = state.grid.map(function(row) {
        return row.slice();
      });

      newGrid[action.position[0]][action.position[1]] = action.color;

      return update(state, {
        grid: newGrid,
      });

    case BLINK_SQUARES:
      return update(state, {
        blinkingSquares: action.positions,
      });

    case UNBLINK_SQUARES:
      return update(state, {
        blinkingSquares: [],
      });

    case START_GAME:
      return update(state, {
        gameInProgress: true,
      });

    case STOP_GAME:
      return update(state, {
        gameInProgress: false,
        nextPlayer: null,
      });

    case REPORT_DRAW:
      return update(state, {
        feedback: `Game ended in a draw`,
      })

    case REPORT_TRY_AGAIN:
      return update(state, {
        feedback: `${action.player.name} try again (${action.reason})`,
      });

    default:
      return state;
  }
}


export default appReducer;
