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


class GameStartButton extends React.Component {
  constructor(props) {
    super(props);
    this.onSubmit = this.onSubmit.bind(this);
  }

  onSubmit(e) {
    e.preventDefault();
    emitStartGame();
  }

  render() {
    const { gameInProgress } = this.props;

    return (
      <div id="game-start">
        <form
          action=""
          method="post"
          onSubmit={this.onSubmit}
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
}


GameStartButton.propTypes = propTypes;

export default connect(mapStateToProps)(GameStartButton);
