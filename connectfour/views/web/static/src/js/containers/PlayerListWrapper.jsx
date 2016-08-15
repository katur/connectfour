import { connect } from 'react-redux'
import PlayerList from "../components/PlayerList";


function mapStateToProps(state) {
  return {
    players: state.players,
  }
}


const PlayerListWrapper = connect(
  mapStateToProps
)(PlayerList);


export default PlayerListWrapper;
