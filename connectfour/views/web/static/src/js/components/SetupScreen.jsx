import React from "react";
import { connect } from "react-redux";
import NewGameForm from "./NewGameForm";
import JoinGameForm from "./JoinGameForm";


function mapStateToProps(state) {
  return {
    show: state.username ? false : true,
  }
}


let SetupScreen = React.createClass({
  render: function() {
    if (!this.props.show) {
      return null;
    }

    return (
      <div id="setup-screen">
        <NewGameForm />
        <JoinGameForm />
      </div>
    );
  },
});


SetupScreen = connect(
  mapStateToProps
)(SetupScreen);


export default SetupScreen;
