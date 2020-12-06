import React, { PropTypes } from 'react';
import { connect } from 'react-redux';
import GameTitle from './GameTitle';
import GameStartButton from './GameStartButton';
import GameRoom from './GameRoom';
import GameFeedback from './GameFeedback';
import GameColumnButtons from './GameColumnButtons';
import GameGrid from './GameGrid';
import GamePlayers from './GamePlayers';
import GameBoardForm from './GameBoardForm';


function mapStateToProps({ room, feedback, numRows, numColumns, grid }) {
  return {
    showRoom: !!room,
    showFeedback: !!feedback,
    showBoard: !!numRows && !!numColumns && !!grid,
  }
}


const propTypes = {
  showRoom: PropTypes.bool.isRequired,
  showFeedback: PropTypes.bool.isRequired,
  showBoard: PropTypes.bool.isRequired,
}


function GameScreen({ showRoom, showFeedback, showBoard }) {
  return (
    <div id="game-screen">
      <div id="top-bar">
        <GameStartButton />

        <GameTitle />

        {showRoom && <GameRoom />}
      </div>


      {showBoard &&
        <div id="game-info">
          <GamePlayers />
          {showFeedback && <GameFeedback />}
          <GameBoardForm />
        </div>
      }

      {showBoard &&
        <div id="game-board">
          <GameColumnButtons />
          <GameGrid />
        </div>
      }
    </div>
  );
}


GameScreen.propTypes = propTypes;

export default connect(mapStateToProps)(GameScreen);
