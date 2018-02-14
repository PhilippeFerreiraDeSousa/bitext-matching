import React, { Component } from 'react'
import { graphql } from 'react-apollo'
import gql from 'graphql-tag'
import { Tab, Pagination } from 'semantic-ui-react'
import AlignerResponse from './AlignerResponse'
import { FetchingErrorMessage } from './ErrorMessage'
import { ALIGNMENTS_PER_PAGE } from '../parameters/constants'

class PaginatedAlignment extends Component {
  state = {
    activePage: 1,
    totalPages: -1
  }

  componentWillReceiveProps(nextProps) {
    if (nextProps.alignmentsNumberQuery && !nextProps.alignmentsNumberQuery.loading) {
      const alignmentInfo = nextProps.alignmentsNumberQuery.alignmentInfo
      this.setState({
        totalPages: Math.ceil(alignmentInfo.progressNumber/ALIGNMENTS_PER_PAGE)
      })
    }
  }

  handlePaginationChange = (e, { activePage }) => {
    this.setState({ activePage })
  }

  render() {
    const { activePage, totalPages } = this.state

    if (this.props.alignmentsNumberQuery && this.props.alignmentsNumberQuery.error) {
      return <FetchingErrorMessage />
    }

    return(
      <Tab.Pane loading={totalPages === -1}>
        <Pagination activePage={activePage} onPageChange={this.handlePaginationChange} totalPages={totalPages} />
        <br />
        <br />
        <AlignerResponse bitextId={this.props.bitextId} page={activePage}/>
      </Tab.Pane>
    )
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
    pollInterval: 5000,
    fetchPolicy: 'network-only'
  })
}) (PaginatedAlignment)
