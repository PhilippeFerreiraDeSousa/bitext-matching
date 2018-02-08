import React, { Component } from 'react'
import { graphql } from 'react-apollo'
import gql from 'graphql-tag'
import { Grid, Segment, List, Icon } from 'semantic-ui-react'

var groupBy = function(xs, key1, key2) {
  return xs.reduce(function(rv, x) {
    (rv[x[key1][key2]] = rv[x[key1][key2]] || []).push(x)
    return rv
  }, {})
}

class Vocabulary extends Component {

  render() {
    const translationsToRender = this.props.translationQuery.translations

    console.log(translationsToRender)

    if (this.props.translationQuery && this.props.translationQuery.loading) {
      return <div>Loading</div>
    }
    if (this.props.translationQuery && this.props.translationQuery.error) {
      return <div>Error</div>
    }
    const wordList = groupBy(translationsToRender, 'word1', 'content')

    return(
      <List>
        { Object.keys(wordList).map( word => (
          <List.Item>
            <List.Icon name='triangle right' />
            <List.Content>
              <List.Header>{word} <Icon name='exchange' /> {wordList[word][0].word2.content}</List.Header>
            </List.Content>
            <br />
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
          </List.Item>
        ))}
      </List>
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
