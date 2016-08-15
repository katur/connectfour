import { connect } from 'react-redux'
import SetupScreen from "../components/SetupScreen";


function mapStateToProps(state) {
  return {
    show: state.username ? false : true,
    defaultRows: window.DEFAULT_ROWS,
    defaultColumns: window.DEFAULT_COLUMNS,
    defaultToWin: window.DEFAULT_TO_WIN,
  }
}


const SetupScreenWrapper = connect(
  mapStateToProps
)(SetupScreen);


export default SetupScreenWrapper;
