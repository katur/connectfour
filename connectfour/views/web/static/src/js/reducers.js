import {
  SET_USERNAME,
  SET_ROOM,
  ADD_PLAYER,
  CREATE_BOARD,
  SET_CURRENT_PLAYER,
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
  currentPlayer: null,
}


// Later, try splitting reducers:
// http://redux.js.org/docs/basics/Reducers.html#splitting-reducers

function appReducer(state = initialState, action) {
  switch(action.type) {

    case SET_USERNAME:
      // Object.assign creates a copy. Consider this instead:
      // http://redux.js.org/docs/recipes/UsingObjectSpreadOperator.html
      return Object.assign({}, state, {
        username: action.username,
      });

    case SET_ROOM:
      return Object.assign({}, state, {
        room: action.room,
      });

    case ADD_PLAYER:
      let player = action.player;

      return Object.assign({}, state, {
        players: [
          ...state.players,
          player,
        ],
        feedback: `Welcome, ${player.name}`,
      });

    case CREATE_BOARD:
      let board = action.board;
      return Object.assign({}, state, {
        numToWin: board.num_to_win,
        numRows: board.num_rows,
        numColumns: board.num_columns,
        grid: board.grid,
        feedback: `${board.num_rows} x ${board.num_columns} board created`,
      });

    default:
      return state;
  }
}


export default appReducer;
