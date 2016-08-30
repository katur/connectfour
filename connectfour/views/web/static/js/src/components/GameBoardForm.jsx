import React from 'react';
import { connect } from 'react-redux';
import Emitters from '../emitters';


function mapStateToProps(state) {
  return {
    gameInProgress: state.gameInProgress,
    numRows: state.numRows,
    numColumns: state.numColumns,
    numToWin: state.numToWin,
  }
}


let ChangeBoardForm = React.createClass({
  propTypes: {
    gameInProgress: React.PropTypes.bool.isRequired,
    numRows: React.PropTypes.number,
    numColumns: React.PropTypes.number,
    numToWin: React.PropTypes.number,
  },

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

    Emitters.createBoard({
      numRows: this.state.numRows,
      numColumns: this.state.numColumns,
      numToWin: this.state.numToWin,
    });
  },

  render: function() {
    return (
      <div id='change-board'>
        <form
          action=''
          method='post'
          onSubmit={this._handleSubmit}
        >
          <dl>
            <dt>Num rows</dt>
            <dd>
              <input
                type='text'
                name='numRows'
                value={this.state.numRows}
                onChange={this._handleInput}
              />
            </dd>

            <dt>Num columns</dt>
            <dd>
              <input
                type='text'
                name='numColumns'
                value={this.state.numColumns}
                onChange={this._handleInput}
              />
            </dd>

            <dt>Num to win</dt>
            <dd>
              <input
                type='text'
                name='numToWin'
                value={this.state.numToWin}
                onChange={this._handleInput}
              />
            </dd>

          </dl>

          <button
            type='submit'
            disabled={this.props.gameInProgress}
          >
            Change board
          </button>
        </form>
      </div>
    );
  },
});


ChangeBoardForm = connect(
  mapStateToProps
)(ChangeBoardForm);


export default ChangeBoardForm;
