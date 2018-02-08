import React, { Component } from 'react'
import { graphql } from 'react-apollo'
import gql from 'graphql-tag'
import { Form, Message, Segment, Grid, Tab } from 'semantic-ui-react'

class AlignerResponse extends Component {

  render() {
    const alignmentsToRender = this.props.alignmentQuery.alignments || []

    console.log(alignmentsToRender)

    if (this.props.alignmentQuery && this.props.alignmentQuery.error) {
      return (
        <Message negative>
          <Message.Header>We&#39;re sorry an error has occured</Message.Header>
          <p>Problem fetching data on the internet</p>
        </Message>
      )
    }
    return(
      <Tab.Pane loading={this.props.alignmentQuery.loading}>
        <Grid columns={2} divided='vertically'>
          {alignmentsToRender.map((alignment, idx) => (
            <Grid.Row key={idx}>
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
      </Tab.Pane>
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
