import React from "react";
import NewGameForm from "./NewGameForm";
import JoinGameForm from "./JoinGameForm";


const SetupScreen = React.createClass({
  render: function() {
    if (this.props.showSetupScreen) {
      return (
        <div id="setup-content">
          <NewGameForm
            defaultRows={this.props.defaultRows}
            defaultColumns={this.props.defaultColumns}
            defaultToWin={this.props.defaultToWin}
          />

          <JoinGameForm/>
        </div>
      );
    } else {
      return null;
    }
  },
});


export default SetupScreen;
