import {
  SET_USERNAME,
  SET_ROOM,
  ADD_PLAYER,
  REMOVE_PLAYER,
  SET_CURRENT_PLAYER_INDEX,
} from "./actions";


const initialState = {
	username: ``,
	room: ``,
	players: [],
	currentPlayerIndex: null,
	board: [[]],
	feedback: ``,
	gameInProgress: false,
	gameNumber: null,
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
      return Object.assign({}, state, {
        players: [
          ...state.players,
          action.player,
        ],
      });

    default:
      return state;
  }
}


export default appReducer;
