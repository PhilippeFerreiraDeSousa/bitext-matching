import React, { Component } from 'react'
import { graphql } from 'react-apollo'
import gql from 'graphql-tag'
import { Form, Message, Segment, Grid } from 'semantic-ui-react'

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
        <Grid columns={2} divided='vertically'>
          {alignmentsToRender.map(alignment => (
            <Grid.Row>
              <Grid.Column>
                <Segment key={alignment.id}>
                  {alignment.paragraphs.filter(paragraph => paragraph.text.language == 'english')
                    .map(paragraph => (
                      <p key={paragraph.id}>
                        {paragraph.sentences.map(sentence => (
                          <span key={sentence.id}>{sentence.content} </span>
                        ))}
                      </p>
                    )
                  )}
                </Segment>
              </Grid.Column>
              <Grid.Column>
                <Segment key={alignment.id}>
                  {alignment.paragraphs.filter(paragraph => paragraph.text.language == 'french')
                    .map(paragraph => (
                      <p key={paragraph.id}>
                        {paragraph.sentences.map(sentence => (
                          <span key={sentence.id}>{sentence.content} </span>
                        ))}
                      </p>
                    )
                  )}
                </Segment>
              </Grid.Column>
            </Grid.Row>
          ))}
        </Grid>
      </div>
    );
  }
}

const ALIGNMENT = gql`
  query alignment($bitextId: Int!) {
    alignments(bitextId: $bitextId) {
      id
      paragraphs {
        id
        text {
          language
        }
        sentences {
          id
          content
        }
    	}
  	}
  }
`

export default graphql(ALIGNMENT, {
  name: 'alignmentQuery',
  options: ({ bitextId: bitextId }) => ({
    variables: { bitextId: bitextId }
  })
}) (AlignerResponse)
