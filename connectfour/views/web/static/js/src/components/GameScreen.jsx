import React from 'react';
import { connect } from 'react-redux';

import GameTitle from './GameTitle';
import GameStartButton from './GameStartButton';
import GameRoom from './GameRoom';
import GameFeedback from './GameFeedback';
import GameColumnButtons from './GameColumnButtons';
import GameGrid from './GameGrid';
import GamePlayers from './GamePlayers';
import GameBoardForm from './GameBoardForm';


function mapStateToProps(state) {
  return {
    showRoom: !!state.room,
    showFeedback: !!state.feedback,
    showBoard: !!state.numRows && !!state.numColumns && !!state.grid,
  }
}


class GameScreen extends React.Component {
  render() {
    const { showRoom, showFeedback, showBoard } = this.props;
    return (
      <div id="game-screen">
        <GameTitle />

        <GameStartButton />

        {showRoom && <GameRoom />}

        {showFeedback && <GameFeedback />}

        {showBoard &&
          <div id="game-board">
            <GameColumnButtons />
            <GameGrid />
          </div>
        }

        <div id="game-control">
          <GamePlayers />
          <GameBoardForm />
        </div>
      </div>
    );
  }
}


GameScreen.propTypes = {
  showRoom: React.PropTypes.bool.isRequired,
  showFeedback: React.PropTypes.bool.isRequired,
  showBoard: React.PropTypes.bool.isRequired,
}


export default connect(mapStateToProps)(GameScreen);
