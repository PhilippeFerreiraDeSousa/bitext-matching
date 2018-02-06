import React, { Component } from 'react'
import { graphql } from 'react-apollo'
import gql from 'graphql-tag'
import { Dropdown } from 'semantic-ui-react'

class BitextList extends Component {
  render() {
    const bitextsToRender = this.props.bitextQuery.allBitexts

    console.log(bitextsToRender)

    if (this.props.bitextQuery && this.props.bitextQuery.loading) {
      return <div>Loading</div>
    }
    if (this.props.bitextQuery && this.props.bitextQuery.error) {
      return <div>Error</div>
    }
    const countryOptions = bitextsToRender.map(bitext => ({key: bitext.id, value: bitext.id, text: bitext.title+(bitext.author ? ' - '+bitext.author : '')}) )
    return(
      <Dropdown placeholder='Select bitext' fluid search selection options={countryOptions} />
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
}) (BitextList)
