import React, { Component } from 'react'
import { graphql } from 'react-apollo'
import gql from 'graphql-tag'
import { Form, Message, Segment } from 'semantic-ui-react'

class AlignerResponse extends Component {

  render() {
    const alignmentsToRender = this.props.alignmentQuery.alignments

    console.log(alignmentsToRender)

    if (this.props.alignmentQuery && this.props.alignmentQuery.loading) {
      return <div>Loading</div>
    }
    if (this.props.alignmentQuery && this.props.alignmentQuery.error) {
      return <div>Error</div>
    }
    return(
      <div>
          {alignmentsToRender.map(alignment => (
            <Segment key={alignment.id}>
              {alignment.paragraphs.map(paragraph => (
                <p key={paragraph.id}>
                  {paragraph.sentences.map(sentence => (
                    <span>{sentence.text}</span>
                  ))}
                </p>
              ))}
            </Segment>
          ))}
      </div>
    );
  }
}

const ALIGNMENT = gql`
  query alignment {
    alignments(bitextId:1) {
      id
      paragraphs {
        id
        text {
          language
        }
        sentences {
          id
          text
        }
    	}
  	}
  }
`

export default graphql(ALIGNMENT, {
  name: 'alignmentQuery',
  options: { pollInterval: 5000 }
}) (AlignerResponse)
