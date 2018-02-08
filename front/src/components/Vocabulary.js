import React, { Component } from 'react'
import { graphql } from 'react-apollo'
import gql from 'graphql-tag'
import { Grid, Segment, Icon, Accordion, Tab, Message } from 'semantic-ui-react'

var groupBy = function(xs, key1, key2) {
  return xs.reduce(function(rv, x) {
    (rv[x[key1][key2]] = rv[x[key1][key2]] || []).push(x)
    return rv
  }, {})
}

class Vocabulary extends Component {
  state = {
    activeIndex: -1
  }

  handleClick = (e, titleProps) => {
    const { index } = titleProps
    const { activeIndex } = this.state
    const newIndex = activeIndex === index ? -1 : index

    this.setState({ activeIndex: newIndex })
  }

  render() {
    const translationsToRender = this.props.translationQuery.translations || []
    const wordList = groupBy(translationsToRender, 'word1', 'content')
    const { activeIndex } = this.state

    if (this.props.translationQuery && this.props.translationQuery.error) {
      return (
        <Message negative>
          <Message.Header>We&#39;re sorry an error has occured</Message.Header>
          <p>Problem fetching data on the internet</p>
        </Message>
      )
    }

    return(
      <Tab.Pane loading={this.props.translationQuery.loading}>
        { Object.keys(wordList).map((word, idx) => (
          <Accordion key={idx}>
            <Accordion.Title active={activeIndex == idx} index={idx} onClick={this.handleClick}>
              <Icon name='triangle right' />
              {word} <Icon name='exchange'/> {wordList[word][0].word2.content}
            </Accordion.Title>
            <Accordion.Content active={activeIndex == idx}>
              <Grid columns={2} stackable={true}>
                {wordList[word].map( translation => (
                  <Grid.Row key={translation.id}>
                    <Grid.Column>
                      <Segment>
                        {translation.sentence1.content}
                      </Segment>
                    </Grid.Column>
                    <Grid.Column>
                      <Segment>
                        {translation.sentence2.content}
                      </Segment>
                    </Grid.Column>
                  </Grid.Row>
                ))}
              </Grid>
            </Accordion.Content>
          </Accordion>
        ))}
      </Tab.Pane>
    )
  }
}

const TRANSLATIONS = gql`
  query translations($bitextId: Int!) {
    translations(bitextId: $bitextId) {
      id
      word1 {
        content
      }
      word2 {
        content
      }
      sentence1 {
        content
      }
      sentence2 {
        content
      }
      score
  	}
  }
`

export default graphql(TRANSLATIONS, {
  name: 'translationQuery',
  options: ({ bitextId }) => ({
    variables: { bitextId: bitextId }
  })
}) (Vocabulary)
