import { connect } from 'react-redux'
import GameScreen from "../components/GameScreen";


function mapStateToProps(state) {
  return {
    show: state.username ? true : false,
  }
}


const GameScreenWrapper = connect(
  mapStateToProps
)(GameScreen);


export default GameScreenWrapper;
