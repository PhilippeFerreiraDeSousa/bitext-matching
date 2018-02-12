import React, { Component } from 'react'
import { graphql } from 'react-apollo'
import gql from 'graphql-tag'
import { Tab, Pagination } from 'semantic-ui-react'
import AlignerResponse from './AlignerResponse'
import { FetchingErrorMessage } from './ErrorMessage'
import { ALIGNMENTS_PER_PAGE } from '../parameters/constants'

class PaginatedAlignment extends Component {
  state = { activePage: 1 }

  handlePaginationChange = (e, { activePage }) => {
    this.setState({ activePage })
  }

  render() {
    const { activePage } = this.state
    const alignmentInfo = this.props.alignmentsNumberQuery.alignmentInfo

    if (this.props.alignmentsNumberQuery && this.props.alignmentsNumberQuery.error) {
      return <FetchingErrorMessage />
    }

    if (this.props.alignmentsNumberQuery && this.props.alignmentsNumberQuery.loading) {
      return <div></div>
    }

    return(
      <Tab.Pane loading={this.props.alignmentsNumberQuery.loading}>
        <Pagination activePage={activePage} onPageChange={this.handlePaginationChange} totalPages={Math.ceil(alignmentInfo.progressNumber/ALIGNMENTS_PER_PAGE)} />
        <br />
        <br />
        <AlignerResponse bitextId={this.props.bitextId} page={activePage}/>
      </Tab.Pane>
    );
  }
}

const ALIGNMENTS_NUMBER = gql`
  query alignmentsNumber($bitextId: Int!) {
    alignmentInfo(id: $bitextId) {
      progressNumber
    }
  }
`

export default graphql(ALIGNMENTS_NUMBER, {
  name: 'alignmentsNumberQuery',
  options: ({ bitextId }) => ({
    variables: { bitextId },
    pollInterval: 5000
  })
}) (PaginatedAlignment)
