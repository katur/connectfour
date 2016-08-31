import React, { PropTypes } from 'react';


const propTypes = {
  blinking: PropTypes.bool.isRequired,
  color: PropTypes.string,
};


function GameSquare({ color, blinking, style }) {
  let innerClassName = `game-square color-${color}`;

  if (blinking) {
    innerClassName += ' blinking';
  }

  return (
    <div
      className="game-square-wrapper"
      style={style}
    >
      <div className={innerClassName} />
    </div>
  );
}


GameSquare.propTypes = propTypes;

export default GameSquare;
