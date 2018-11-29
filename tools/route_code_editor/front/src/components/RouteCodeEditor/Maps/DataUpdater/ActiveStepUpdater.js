import React from 'react';
import {connect} from "react-redux";

class ActiveStepUpdater extends React.Component {
  constructor(props) {
    super(props);
  }

  componentDidUpdate() {
    console.log(this.props);
    if (this.props.activeStep !== undefined) {
      this.props.setActiveStep(this.props.activeStep);
    }
  }

  render() {
    return (<div/>)
  }
}

const mapState = (state) => ({
  activeStep: state.routeCodeEditor.getActiveStep()
});


const mapDispatch = () => ({});

export default connect(mapState, mapDispatch)(ActiveStepUpdater);