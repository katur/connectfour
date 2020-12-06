import React, { PropTypes } from 'react';
import { connect } from 'react-redux';
import SetupScreen from './SetupScreen';
import GameScreen from './GameScreen';


function mapStateToProps({ room }) {
  return {
    showGameScreen: room ? true : false,
  };
}


const propTypes = {
  showGameScreen: PropTypes.bool.isRequired,
};


function App({ showGameScreen }) {
  return (
    <div>
      {showGameScreen ? <GameScreen /> : <SetupScreen />}
    </div>
  );
}


App.propTypes = propTypes;

export default connect(mapStateToProps)(App);
