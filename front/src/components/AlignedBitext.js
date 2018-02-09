import React, { Component } from 'react'
import { graphql } from 'react-apollo'
import gql from 'graphql-tag'
import { Dropdown } from 'semantic-ui-react'
import BitextData from './BitextData'
import ErrorMessage from './ErrorMessage'

class AlignedBitext extends Component {
  state = {
    bitextId: null
  }

  handleInputChange = (event, { value }) => {
    this.setState({
        bitextId: value
    })
  }

  render() {
    const bitextsToRender = this.props.bitextQuery.allBitexts
    var bitextOptions =  []

    //if (this.state.loadingAlignment) {
    //  this.handleLoading('loadingAlignment', false)
    //}

    if (this.props.bitextQuery && this.props.bitextQuery.error) {
      return <ErrorMessage />
    }
    if (this.props.bitextQuery && !this.props.bitextQuery.loading) {
      bitextOptions = bitextsToRender.map(bitext => ({key: bitext.id, value: bitext.id, text: bitext.title+(bitext.author ? ' - '+bitext.author : '')}) )
    }

    return(
      <div>
        <Dropdown placeholder='Select bitext' fluid search selection options={bitextOptions} onChange={this.handleInputChange} loading={this.props.bitextQuery && this.props.bitextQuery.loading} />
        <br />
        <BitextData bitextId={this.state.bitextId}/>
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
  //options: { pollInterval: 5000 }
}) (AlignedBitext)
