import React, { Component } from 'react'
import { graphql } from 'react-apollo'
import gql from 'graphql-tag'
import { Progress } from 'semantic-ui-react'
import BitextData from './BitextData'
import { FetchingErrorMessage } from './ErrorMessage'

class ResponseProgress extends Component {
  render() {
    const alignmentInfo = this.props.alignmentsNumberQuery.alignmentInfo

    if (this.props.alignmentsNumberQuery && this.props.alignmentsNumberQuery.error) {
      return <FetchingErrorMessage />
    }

    if (this.props.alignmentsNumberQuery && this.props.alignmentsNumberQuery.loading) {
      return <div></div>
    }
    console.log(alignmentInfo.progressNumber)
    console.log(alignmentInfo.alignmentsNumber)

    return(
      <div>
        <Progress percent={Math.round(100*alignmentInfo.progressNumber/alignmentInfo.alignmentsNumber) || 0} progress autoSuccess>
          Alignment in progress
        </Progress>
        <BitextData bitextId={this.props.bitextId}/>
      </div>
    );
  }
}

const ALIGNMENTS_NUMBER = gql`
  query alignmentsNumber($bitextId: Int!) {
    alignmentInfo(id: $bitextId) {
      alignmentsNumber
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
}) (ResponseProgress)
