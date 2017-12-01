import React, { Component } from 'react'
import { graphql } from 'react-apollo'
import gql from 'graphql-tag'

class Aligner extends Component {
  render() {
    const linksToRender = this.props.allLinksQuery.allLinks
    console.log(linksToRender)
    if (this.props.allLinksQuery && this.props.allLinksQuery.loading) {
      return <div>Loading</div>
    }
    if (this.props.allLinksQuery && this.props.allLinksQuery.error) {
      return <div>Error</div>
    }
    return(
      <section className='App-body'>
        <h2>Let&#39;s align bitexts !</h2>
        <p>
          {linksToRender[0].description}
        </p>
      </section>
    );
  }
}

const ALL_LINKS_QUERY = gql`
  query AllLinksQuery {
    allLinks {
      id
      createdAt
      url
      description
    }
  }
`

export default graphql(ALL_LINKS_QUERY, { name: 'allLinksQuery' }) (Aligner)
