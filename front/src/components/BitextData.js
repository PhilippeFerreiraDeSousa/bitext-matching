import React, { Component } from 'react'
import { graphql } from 'react-apollo'
import gql from 'graphql-tag'
import { Tab } from 'semantic-ui-react'
import AlignerResponse from './AlignerResponse'
import Vocabulary from './Vocabulary'

class AlignedBitext extends Component {
  panes = [
    { menuItem: 'Alignment', render: () => (
      <AlignerResponse bitextId={this.props.bitextId}/>
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