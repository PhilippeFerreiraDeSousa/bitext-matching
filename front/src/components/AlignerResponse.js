import React, { Component } from 'react'
import { graphql } from 'react-apollo'
import gql from 'graphql-tag'
import { Segment, Grid, Tab } from 'semantic-ui-react'
import ErrorMessage from './ErrorMessage'

class AlignerResponse extends Component {

  render() {
    const alignmentsToRender = this.props.alignmentQuery.alignments || []

    if (this.props.alignmentQuery && this.props.alignmentQuery.error) {
      return <ErrorMessage />
    }

    if (this.props.alignmentQuery && this.props.alignmentQuery.loading) {
      return <div></div>
    }
    const languages = this.props.alignmentQuery.bitext.texts.map((text) => text.language)   // it would be proper to group by instead of fetching the languages

    return(
      <Tab.Pane loading={this.props.alignmentQuery.loading}>
        <Grid columns={2} divided='vertically'>
          {alignmentsToRender.map((alignment, idx) => (
            <Grid.Row key={idx}>
              <Grid.Column>
                <Segment key={alignment.id}>
                  {alignment.paragraphs.filter(paragraph => paragraph.text.language === languages[0])
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
                  {alignment.paragraphs.filter(paragraph => paragraph.text.language === languages[1])
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
    bitext(id: $bitextId) {
      texts {
        language
      }
    }
  }
`

export default graphql(ALIGNMENT, {
  name: 'alignmentQuery',
  options: ({ bitextId }) => ({
    variables: { bitextId: bitextId }
  })
}) (AlignerResponse)
