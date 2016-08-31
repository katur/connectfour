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
  numRows: PropTypes.number.isRequired,
  numColumns: PropTypes.number.isRequired,
  numToWin: PropTypes.number.isRequired,
};


class GameBoardForm extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      numRows: props.numRows,
      numColumns: props.numColumns,
      numToWin: props.numToWin,
      username: '',
    };

    // Bind callbacks to make `this` the correct context
    this._handleInput = this._handleInput.bind(this);
    this._handleSubmit = this._handleSubmit.bind(this);
  }

  componentWillReceiveProps({ numRows, numColumns, numToWin }) {
    this.setState({
      numRows,
      numColumns,
      numToWin,
    });
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
      <div id="game-board-form">
        <form
          action=""
          method="post"
          onSubmit={this._handleSubmit}
        >
          <dl>
            <dt>Rows</dt>
            <dd>
              <input
                type="text"
                name="numRows"
                value={numRows}
                onChange={this._handleInput}
              />
            </dd>

            <dt>Columns</dt>
            <dd>
              <input
                type="text"
                name="numColumns"
                value={numColumns}
                onChange={this._handleInput}
              />
            </dd>

            <dt>To win</dt>
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
            Change
          </button>
        </form>
      </div>
    );
  }
}


GameBoardForm.propTypes = propTypes;

export default connect(mapStateToProps)(GameBoardForm);
