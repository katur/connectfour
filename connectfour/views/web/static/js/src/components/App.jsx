import React from 'react';
import { connect } from 'react-redux';

import SetupScreen from './SetupScreen';
import GameScreen from './GameScreen';


function mapStateToProps(state) {
  return {
    showGameScreen: state.room ? true : false,
  }
}


class App extends React.Component {
  render() {
    const { showGameScreen } = this.props;

    return (
      <div>
        {showGameScreen ? <GameScreen /> : <SetupScreen />}
      </div>
    );
  }
}


App.propTypes = {
  showGameScreen: React.PropTypes.bool.isRequired,
}


export default connect(mapStateToProps)(App);
