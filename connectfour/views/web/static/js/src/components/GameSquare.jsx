import React from "react";


const GameSquare = React.createClass({
  propTypes: {
    blinking: React.PropTypes.bool.isRequired,
    color: React.PropTypes.string,
  },

  render: function() {
    let innerClassName = `game-square color-${this.props.color}`;

    if (this.props.blinking) {
      innerClassName += " blinking";
    }

    return (
      <div
        className="game-square-wrapper"
        style={this.props.style}
      >
        <div
          className={innerClassName}
        >
        </div>
      </div>
    );
  },
});


export default GameSquare;
