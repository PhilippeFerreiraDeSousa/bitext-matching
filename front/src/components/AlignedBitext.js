import React, { Component } from 'react'
import { graphql } from 'react-apollo'
import gql from 'graphql-tag'
import { Dropdown, Tab } from 'semantic-ui-react'
import AlignerResponse from './AlignerResponse'

class AlignedBitext extends Component {
  state = {
    bitextId: null
  }

  panes = [
    { menuItem: 'Alignment', render: () => (
      <Tab.Pane>{ this.state.bitextId ? <AlignerResponse bitextId={this.state.bitextId} /> : null }</Tab.Pane>
    )},
    { menuItem: 'Vocabulary', render: () => (
      <Tab.Pane>Some vocab</Tab.Pane>
    )}
  ]

  handleInputChange = (event, { name, value }) => {
    this.setState({
        bitextId: value
    });
  }

  render() {
    const bitextsToRender = this.props.bitextQuery.allBitexts
    var bitextOptions =  []

    console.log(bitextsToRender)

    if (this.props.bitextQuery && this.props.bitextQuery.error) {
      return <div>Error</div>
    }
    if (this.props.bitextQuery && !this.props.bitextQuery.loading) {
      bitextOptions = bitextsToRender.map(bitext => ({key: bitext.id, value: bitext.id, text: bitext.title+(bitext.author ? ' - '+bitext.author : '')}) )
    }

    return(
      <div>
        <Dropdown placeholder='Select bitext' fluid search selection options={bitextOptions} onChange={this.handleInputChange} loading={this.props.bitextQuery && this.props.bitextQuery.loading} />
        <br />
        <Tab panes={this.panes} />
      </div>
    );
  }
}

const BITEXTS = gql`
  query bitexts {
    allBitexts {
      id
      title
      author
  	}
  }
`

export default graphql(BITEXTS, {
  name: 'bitextQuery',
  options: { pollInterval: 5000 }
}) (AlignedBitext)
