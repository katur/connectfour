import React from "react";
import { connect } from 'react-redux'


function mapStateToProps(state) {
  return {
    numToWin: state.numToWin,
  }
}


let GameTitle = React.createClass({
  render: function() {
    return (
      <div>
        <h1>
          Connect {this.props.numToWin}
        </h1>
      </div>
    );
  },
});


GameTitle = connect(
  mapStateToProps
)(GameTitle);


export default GameTitle;
