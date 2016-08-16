import React from "react";
import SetupScreen from "./SetupScreen";
import GameScreen from "./GameScreen";


const App = React.createClass({
  render: function() {
    return (
      <div>
      <SetupScreen />
      <GameScreen />
      </div>
    );
  },
});


export default App;
