import React, { Component } from 'react'
import { Tab } from 'semantic-ui-react'
import AlignerResponse from './AlignerResponse'
import Vocabulary from './Vocabulary'

class AlignedBitext extends Component {
  panes = [
    { menuItem: 'Alignment', render: () => (
      <AlignerResponse bitextId={this.props.bitext.id}/>
    )},
    { menuItem: 'Vocabulary', render: () => (
      <Vocabulary bitextId={this.props.bitext.id}/>
    )}
  ]

  render() {
    return(
      <div>
        { this.props.bitext.id ? <Tab panes={this.panes} /> : null }
      </div>
    );
  }
}

export default AlignedBitext
