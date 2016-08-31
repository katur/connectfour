import React, { PropTypes } from 'react';
import { connect } from 'react-redux';
import { emitCreateBoard } from '../emitters';


function mapStateToProps({ gameInProgress, numRows, numColumns, numToWin }) {
  return {
    gameInProgress,
    numRows,
    numColumns,
    numToWin,
  };
}


const propTypes = {
  gameInProgress: PropTypes.bool.isRequired,
  numRows: PropTypes.number,
  numColumns: PropTypes.number,
  numToWin: PropTypes.number,
};


class GameBoardForm extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      numRows: `${window.DEFAULT_ROWS}`,
      numColumns: `${window.DEFAULT_COLUMNS}`,
      numToWin: `${window.DEFAULT_TO_WIN}`,
      username: ``,
    };

    // Bind callbacks to make `this` the correct context
    this._handleInput = this._handleInput.bind(this);
    this._handleSubmit = this._handleSubmit.bind(this);
  }

  _handleInput(e) {
    this.setState({
      [e.target.name]: e.target.value,
    });
  }

  _handleSubmit(e) {
    e.preventDefault();

    emitCreateBoard({
      numRows: this.state.numRows,
      numColumns: this.state.numColumns,
      numToWin: this.state.numToWin,
    });
  }

  render() {
    const { numRows, numColumns, numToWin } = this.state;
    const { gameInProgress } = this.props;

    return (
      <div id="change-board">
        <form
          action=""
          method="post"
          onSubmit={this._handleSubmit}
        >
          <dl>
            <dt>Num rows</dt>
            <dd>
              <input
                type="text"
                name="numRows"
                value={numRows}
                onChange={this._handleInput}
              />
            </dd>

            <dt>Num columns</dt>
            <dd>
              <input
                type="text"
                name="numColumns"
                value={numColumns}
                onChange={this._handleInput}
              />
            </dd>

            <dt>Num to win</dt>
            <dd>
              <input
                type="text"
                name="numToWin"
                value={numToWin}
                onChange={this._handleInput}
              />
            </dd>

          </dl>

          <button
            type="submit"
            disabled={gameInProgress}
          >
            Change board
          </button>
        </form>
      </div>
    );
  }
}


GameBoardForm.propTypes = propTypes;

export default connect(mapStateToProps)(GameBoardForm);
