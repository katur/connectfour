import {
  SET_ROOM_DOES_NOT_EXIST, SET_LOGGED_IN_USER,
  INITIALIZE_BOARD, INITIALIZE_PLAYERS,
  ADD_PLAYER, REMOVE_PLAYER,
  START_GAME, SET_NEXT_PLAYER, COLOR_SQUARE, TRY_AGAIN,
  GAME_WON, GAME_DRAW,
} from "./actions";


const initialState = {
  username: ``,
  pk: ``,
  room: ``,
  roomDoesNotExist: false,

  gameNumber: 0,
  gameInProgress: false,
  feedback: ``,

  grid: [[]],
  numRows: null,
  numColumns: null,
  numToWin: null,

  players: [],
  nextPlayer: null,
}


function update(state, mutations) {
  return Object.assign({}, state, mutations);
}


// Later, try splitting reducers:
// http://redux.js.org/docs/basics/Reducers.html#splitting-reducers

// Also later, try using object spread operator
// http://redux.js.org/docs/recipes/UsingObjectSpreadOperator.html

function appReducer(state = initialState, action) {
  switch(action.type) {

    case SET_ROOM_DOES_NOT_EXIST:
      return update(state, {
        roomDoesNotExist: true,
      });

    case SET_LOGGED_IN_USER:
      return update(state, {
        username: action.username,
        pk: action.pk,
        room: action.room,
      });

    case INITIALIZE_PLAYERS:
      return update(state, {
        players: action.players,
      });

    case INITIALIZE_BOARD:
      return update(state, {
        numRows: action.board.numRows,
        numColumns: action.board.numColumns,
        numToWin: action.board.numToWin,
        grid: action.board.grid,
      });

    case ADD_PLAYER:
      return update(state, {
        players: [
          ...state.players,
          action.player,
        ],
        feedback: `${action.player.name} has joined the room`,
      });

    case REMOVE_PLAYER:
      var newPlayers = state.players.filter(function(player) {
        return player.pk !== action.player.pk;
      });

      return update(state, {
        players: newPlayers,
        feedback: `${action.player.name} has left the room`,
      });

    case START_GAME:
      return update(state, {
        gameNumber: action.gameNumber,
        gameInProgress: true,
      });

    case SET_NEXT_PLAYER:
      return update(state, {
        nextPlayer: action.player,
        feedback: `${action.player.name} turn`,
      });

    case COLOR_SQUARE:
      var newGrid = state.grid.map(function(row) {
        return row.slice();
      });

      newGrid[action.position[0]][action.position[1]] = action.color;

      return update(state, {
        grid: newGrid,
      });

    case TRY_AGAIN:
      return update(state, {
        feedback: `${action.player.name} try again (${action.reason})`,
      });

    case GAME_WON:
      var newPlayers = state.players.map(function(player) {
        return (player.pk === action.player.pk) ? action.player : player;
      });

      return update(state, {
        players: newPlayers,
        gameInProgress: false,
        nextPlayer: null,
        feedback: `Game won by ${action.player.name}`,
      })

    case GAME_DRAW:
      return update(state, {
        gameInProgress: false,
        nextPlayer: null,
        feedback: `Game ended in a draw`,
      })

    default:
      return state;
  }
}


export default appReducer;
