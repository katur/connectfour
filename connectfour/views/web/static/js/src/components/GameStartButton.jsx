import React from 'react';
import { connect } from 'react-redux';
import Emitters from '../emitters';


function mapStateToProps(state) {
  return {
    gameInProgress: state.gameInProgress,
  }
}


let GameStartButton = React.createClass({
  propTypes: {
    gameInProgress: React.PropTypes.bool.isRequired,
  },

  _handleSubmit: function(e) {
    e.preventDefault();
    Emitters.startGame();
  },

  render: function() {
    return (
      <div id='game-start'>
        <form
          action=''
          method='post'
          onSubmit={this._handleSubmit}
        >
          <button
            type='submit'
            disabled={this.props.gameInProgress}
          >
            Start Game
          </button>
        </form>
      </div>
    );
  },
});


GameStartButton = connect(
  mapStateToProps
)(GameStartButton);


export default GameStartButton;
