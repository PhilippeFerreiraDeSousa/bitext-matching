import React, { Component } from 'react'
import { Tab } from 'semantic-ui-react'
import PaginatedAlignment from './PaginatedAlignment'
import Vocabulary from './Vocabulary'

class AlignedBitext extends Component {
  panes = [
    { menuItem: 'Alignment', render: () => (
      <PaginatedAlignment bitextId={this.props.bitextId}/>
    )},
    { menuItem: 'Vocabulary', render: () => (
      <Vocabulary bitextId={this.props.bitextId}/>
    )}
  ]

  render() {
    return(
      <div>
        { this.props.bitextId ? <Tab panes={this.panes} /> : null }
      </div>
    );
  }
}

export default AlignedBitext
