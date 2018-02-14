import React, { Component } from 'react'
import { graphql } from 'react-apollo'
import gql from 'graphql-tag'
import { Progress } from 'semantic-ui-react'
import BitextData from './BitextData'
import { FetchingErrorMessage } from './ErrorMessage'

class ResponseProgress extends Component {
  state = {
    progress: 0
  }

  componentWillReceiveProps(nextProps) {
    if (nextProps.alignmentsNumberQuery && !nextProps.alignmentsNumberQuery.loading && nextProps.alignmentsNumberQuery.alignmentInfo) {
      const alignmentInfo = nextProps.alignmentsNumberQuery.alignmentInfo
      this.setState({
        progress: Math.round(100*alignmentInfo.progressNumber/alignmentInfo.alignmentsNumber)
      })
      console.log(alignmentInfo.progressNumber)
      console.log(alignmentInfo.alignmentsNumber)
    }
  }

  render() {
    const { progress } = this.state

    if (this.props.alignmentsNumberQuery && this.props.alignmentsNumberQuery.error) {
      return <FetchingErrorMessage />
    }

    return(
      <div>
        <Progress percent={progress} progress autoSuccess>
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
    pollInterval: 5000,
    fetchPolicy: 'no-cache'
  })
}) (ResponseProgress)
