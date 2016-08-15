import React from "react";
import GameScreenWrapper from "../containers/GameScreenWrapper";
import SetupScreenWrapper from "../containers/SetupScreenWrapper";


const App = React.createClass({
  render: function() {
    return (
      <div>
      <SetupScreenWrapper />
      <GameScreenWrapper />
      </div>
    );
  },
});


export default App;
