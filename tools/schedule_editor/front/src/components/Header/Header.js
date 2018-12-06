import React from 'react';
import {connect} from "react-redux";
import {bindActionCreators} from "redux";

import * as ScheduleEditorActions from "../../redux/Actions/ScheduleEditorActions";
import {AppBar, Button, Toolbar, Typography} from "@material-ui/core";
import CloudUploadOutlined from '@material-ui/icons/CloudUploadOutlined';

import ImportDataModal from './ImportDataModal';

class Header extends React.Component {

  constructor(props) {
    super(props);
    this.isWaypointAndLaneLoaderOpen = this.isWaypointAndLaneLoaderOpen.bind(this);
  }

  isWaypointAndLaneLoaderOpen() {
    this.props.scheduleEditorActions.setIsImportDataModalOpen(true);
    console.log("test");
  }

  render() {
    return (
      <div style={{flexGrow: 1}}>
        <AppBar position="static">
          <Toolbar>
            <Typography variant="h6" color="inherit" style={{flexGrow: 1}}>
              Schedule Editor
            </Typography>
            <Button
              style={{color: 'white'}}
              color="default"
              onClick={this.isWaypointAndLaneLoaderOpen}
            >
              Import Map Data
              <CloudUploadOutlined style={{color: 'white', marginLeft: '5px'}} />
            </Button>
            <ImportDataModal/>
          </Toolbar>
        </AppBar>
      </div>
    );
  }
}

const mapState = () => ({});

const mapDispatch = (dispatch) => ({
  scheduleEditorActions: bindActionCreators(ScheduleEditorActions, dispatch),

});

export default connect(mapState, mapDispatch)(Header);
