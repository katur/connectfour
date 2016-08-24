import {
  SET_IDS, SET_ROOM_DOES_NOT_EXIST,
  SET_PLAYERS, ADD_PLAYER, REMOVE_PLAYER, SET_NEXT_PLAYER,
  SET_BOARD, START_GAME, COLOR_SQUARE, TRY_AGAIN, GAME_WON, GAME_DRAW,
} from "./actions";


const initialState = {
  pk: ``,
  room: ``,
  roomDoesNotExist: false,

  gameNumber: 0,
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


// Later, try splitting reducers:
// http://redux.js.org/docs/basics/Reducers.html#splitting-reducers

// Also later, try using object spread operator
// http://redux.js.org/docs/recipes/UsingObjectSpreadOperator.html

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

    case SET_PLAYERS:
      return update(state, {
        players: action.players,
      });

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

    case SET_BOARD:
      return update(state, {
        numRows: action.board.numRows,
        numColumns: action.board.numColumns,
        numToWin: action.board.numToWin,
        grid: action.board.grid,
        blinkingSquares: [],
      });

    case START_GAME:
      return update(state, {
        gameNumber: action.gameNumber,
        gameInProgress: true,
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
        blinkingSquares: action.winningPositions,
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
