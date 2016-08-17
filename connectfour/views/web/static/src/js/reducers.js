import {
  SET_USERNAME,
  SET_ROOM,
  INITIALIZE_BOARD,
  INITIALIZE_PLAYERS,
  ADD_PLAYER,
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

    case INITIALIZE_PLAYERS:
      return Object.assign({}, state, {
        players: action.players,
      });

    case INITIALIZE_BOARD:
      let newState = Object.assign({}, state, {
        numRows: action.board.num_rows,
        numColumns: action.board.num_columns,
        numToWin: action.board.num_to_win,
        grid: action.board.grid,
      });
      return newState;

    case ADD_PLAYER:
      let player = action.player;

      return Object.assign({}, state, {
        players: [
          ...state.players,
          player,
        ],
        feedback: `Welcome, ${player.name}`,
      });

    default:
      return state;
  }
}


export default appReducer;
