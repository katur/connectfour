import React, { PropTypes } from 'react';
import { emitPlay } from '../emitters';


const propTypes = {
  disabled: PropTypes.bool.isRequired,
  style: PropTypes.object.isRequired,
}


const GameColumnButton = React.createClass({
  _handleSubmit: function(e) {
    e.preventDefault();

    emitPlay({
      column: this.props.column,
    });
  },

  render: function() {
    return (
      <form
        action=""
        method="post"
        onSubmit={this._handleSubmit}
      >
        <div
          className="game-column-button-wrapper"
          style={this.props.style}
        >
          <button
            className="game-column-button"
            disabled={this.props.disabled}
          >
            Drop
          </button>
        </div>
      </form>
    );
  },
});


GameColumnButton.propTypes = propTypes;

export default GameColumnButton;
