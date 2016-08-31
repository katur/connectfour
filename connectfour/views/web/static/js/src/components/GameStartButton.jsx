import React, { PropTypes } from 'react';
import { connect } from 'react-redux';
import { emitStartGame } from '../emitters';


function mapStateToProps({ gameInProgress }) {
  return {
    gameInProgress,
  };
}


const propTypes = {
  gameInProgress: PropTypes.bool.isRequired,
};


function GameStartButton({ gameInProgress }) {
  return (
    <div id="game-start">
      <form
        action=""
        method="post"
        onSubmit={(e) => {
          e.preventDefault();
          emitStartGame();
        }}
      >
        <button
          type="submit"
          disabled={gameInProgress}
        >
          Start Game
        </button>
      </form>
    </div>
  );
}


GameStartButton.propTypes = propTypes;

export default connect(mapStateToProps)(GameStartButton);
