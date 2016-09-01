import React, { PropTypes } from 'react';
import { emitPlay } from '../emitters';


const propTypes = {
  column: PropTypes.number.isRequired,
  disabled: PropTypes.bool.isRequired,
  style: PropTypes.object.isRequired,
}


class GameColumnButton extends React.Component {
  constructor(props) {
    super(props);

    // Bind callbacks to make `this` the correct context
    this._handleSubmit = this._handleSubmit.bind(this);
  }

  _handleSubmit(e) {
    e.preventDefault();
    emitPlay({
      column: this.props.column,
    });
  }

  render() {
    const { style, disabled } = this.props;

    return (
      <form
        action=""
        method="post"
        onSubmit={this._handleSubmit}
      >
        <div
          className="game-column-button-wrapper"
          style={style}
        >
          <button
            className="game-column-button"
            disabled={disabled}
          >
            ↓
          </button>
        </div>
      </form>
    );
  }
}


GameColumnButton.propTypes = propTypes;

export default GameColumnButton;
