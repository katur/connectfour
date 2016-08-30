import React from 'react';
import { connect } from 'react-redux';

import SetupScreen from './SetupScreen';
import GameScreen from './GameScreen';


function mapStateToProps(state) {
  return {
    showGameScreen: state.room ? true : false,
  }
}


let App = React.createClass({
  propTypes: {
    showGameScreen: React.PropTypes.bool.isRequired,
  },

  render: function() {
    return (
      <div>
        {this.props.showGameScreen ? <GameScreen /> : <SetupScreen />}
      </div>
    );
  },
});


App = connect(
  mapStateToProps
)(App);


export default App;
