import {
  SET_USERNAME,
  SET_ROOM,
  INITIALIZE_BOARD,
  INITIALIZE_PLAYERS,
  ADD_PLAYER,
  REMOVE_PLAYER,
  START_GAME,
  SET_NEXT_PLAYER,
  COLOR_SQUARE,
  TRY_AGAIN,
  GAME_WON,
  GAME_DRAW,
} from "./actions";


const initialState = {
  username: ``,
  room: ``,

  gameNumber: null,
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

function appReducer(state = initialState, action) {
  switch(action.type) {

    case SET_USERNAME:
      // Object.assign creates a copy. Consider this instead:
      // http://redux.js.org/docs/recipes/UsingObjectSpreadOperator.html
      return update(state, {
        username: action.username,
      });

    case SET_ROOM:
      return update(state, {
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
      var newPlayers = state.players.slice();
      var indexToRemove = newPlayers.indexOf(action.player);
      newPlayers.splice(indexToRemove, 1);

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
      return update(state, {
        gameInProgress: false,
        feedback: `Game won by ${action.player.name}`,
      })

    case GAME_DRAW:
      return update(state, {
        gameInProgress: false,
        feedback: `Game ended in a draw`,
      })

    default:
      return state;
  }
}


export default appReducer;
