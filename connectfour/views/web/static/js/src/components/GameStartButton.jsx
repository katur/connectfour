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


const GameStartButton = React.createClass({
  _handleSubmit: function(e) {
    e.preventDefault();
    emitStartGame();
  },

  render: function() {
    return (
      <div id="game-start">
        <form
          action=""
          method="post"
          onSubmit={this._handleSubmit}
        >
          <button
            type="submit"
            disabled={this.props.gameInProgress}
          >
            Start Game
          </button>
        </form>
      </div>
    );
  },
});


GameStartButton.propTypes = propTypes;

export default connect(mapStateToProps)(GameStartButton);
