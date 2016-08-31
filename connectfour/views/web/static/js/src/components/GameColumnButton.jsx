import React, { PropTypes } from 'react';
import { emitPlay } from '../emitters';


const propTypes = {
  column: PropTypes.number.isRequired,
  disabled: PropTypes.bool.isRequired,
  style: PropTypes.object.isRequired,
}


function GameColumnButton({ column, style, disabled }) {
  return (
    <form
      action=""
      method="post"
      onSubmit={(e) => {
        e.preventDefault();
        emitPlay({
          column: column,
        });
      }}
    >
      <div
        className="game-column-button-wrapper"
        style={style}
      >
        <button
          className="game-column-button"
          disabled={disabled}
        >
          Drop
        </button>
      </div>
    </form>
  );
}


GameColumnButton.propTypes = propTypes;

export default GameColumnButton;
