import React from "react";
import { connect } from "react-redux";
import NewGameForm from "./NewGameForm";
import JoinGameForm from "./JoinGameForm";


function mapStateToProps(state) {
  return {
    show: state.username ? false : true,
    defaultRows: window.DEFAULT_ROWS,
    defaultColumns: window.DEFAULT_COLUMNS,
    defaultToWin: window.DEFAULT_TO_WIN,
  }
}


var SetupScreen = React.createClass({
  render: function() {
    if (!this.props.show) {
      return null;
    }

    return (
      <div id="setup-screen">
        <NewGameForm
          defaultRows={this.props.defaultRows}
          defaultColumns={this.props.defaultColumns}
          defaultToWin={this.props.defaultToWin}
        />

        <JoinGameForm/>
      </div>
    );
  },
});


SetupScreen = connect(
  mapStateToProps
)(SetupScreen);


export default SetupScreen;
