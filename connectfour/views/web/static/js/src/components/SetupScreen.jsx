import React from "react";
import { connect } from "react-redux";
import CreateRoomForm from "./CreateRoomForm";
import JoinRoomForm from "./JoinRoomForm";


function mapStateToProps(state) {
  return {
    show: state.room ? false : true,
  }
}


let SetupScreen = React.createClass({
  render: function() {
    if (!this.props.show) {
      return null;
    }

    return (
      <div id="setup-screen">
        <h1>Connect X</h1>
        <CreateRoomForm />
        <JoinRoomForm />
      </div>
    );
  },
});


SetupScreen = connect(
  mapStateToProps
)(SetupScreen);


export default SetupScreen;
