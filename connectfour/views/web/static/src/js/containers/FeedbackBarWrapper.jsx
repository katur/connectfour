import { connect } from 'react-redux'
import FeedbackBar from "../components/FeedbackBar";


function mapStateToProps(state) {
  return {
    text: state.feedback,
  }
}


const FeedbackBarWrapper = connect(
  mapStateToProps
)(FeedbackBar);


export default FeedbackBarWrapper;
