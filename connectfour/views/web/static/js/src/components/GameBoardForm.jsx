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


const GameBoardForm = React.createClass({
  getInitialState: function() {
    return {
      numRows: `${window.DEFAULT_ROWS}`,
      numColumns: `${window.DEFAULT_COLUMNS}`,
      numToWin: `${window.DEFAULT_TO_WIN}`,
      username: ``,
    };
  },

  _handleInput: function(e) {
    this.setState({
      [e.target.name]: e.target.value,
    });
  },

  _handleSubmit: function(e) {
    e.preventDefault();

    emitCreateBoard({
      numRows: this.state.numRows,
      numColumns: this.state.numColumns,
      numToWin: this.state.numToWin,
    });
  },

  render: function() {
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
                value={this.state.numRows}
                onChange={this._handleInput}
              />
            </dd>

            <dt>Num columns</dt>
            <dd>
              <input
                type="text"
                name="numColumns"
                value={this.state.numColumns}
                onChange={this._handleInput}
              />
            </dd>

            <dt>Num to win</dt>
            <dd>
              <input
                type="text"
                name="numToWin"
                value={this.state.numToWin}
                onChange={this._handleInput}
              />
            </dd>

          </dl>

          <button
            type="submit"
            disabled={this.props.gameInProgress}
          >
            Change board
          </button>
        </form>
      </div>
    );
  },
});


GameBoardForm.propTypes = propTypes;

export default connect(mapStateToProps)(GameBoardForm);
