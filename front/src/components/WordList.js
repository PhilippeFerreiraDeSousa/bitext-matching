import React, { Component } from 'react'
import { graphql } from 'react-apollo'
import gql from 'graphql-tag'
import { Grid, Segment, List } from 'semantic-ui-react'

var groupBy = function(xs, key1, key2) {
  return xs.reduce(function(rv, x) {
    (rv[x[key1][key2]] = rv[x[key1][key2]] || []).push(x)
    return rv
  }, {})
}

class WordList extends Component {

  render() {
    const translationsToRender = this.props.translationQuery.translations
    const language = this.props.language

    console.log(translationsToRender)

    if (this.props.translationQuery && this.props.translationQuery.loading) {
      return <div>Loading</div>
    }
    if (this.props.translationQuery && this.props.translationQuery.error) {
      return <div>Error</div>
    }
    const wordList = groupBy(translationsToRender, language === 'english' ? 'word2' : 'word1', 'content')

    return(
      <List>
        { Object.keys(wordList).map( word => (
          <List.Item>
            <List.Icon name='arrow right' />
            <List.Content>
              <List.Header>{word}</List.Header>
            </List.Content>
            <List.List>
              {wordList[word].map( translation => (
                <List.Item key={translation.id}>
                  <List.Icon name='book' />
                  <List.Content>
                    <List.Header>{translation.bitext.title}</List.Header>
                    <List.Description>{translation.bitext.author}</List.Description>
                  </List.Content>
                  <Grid columns={2} divided='vertically'>
                    <Grid.Row>
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
                  </Grid>
                </List.Item>
              ))}
            </List.List>
          </List.Item>
        ))}
      </List>
    )

  }
}

const TRANSLATIONS = gql`
  query translations($wordId: Int!) {
    translations(wordId: $wordId) {
      id
      bitext {
        title
        author
      }
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
  options: ({ wordId }) => ({
    variables: { wordId: wordId }
  })
}) (WordList)
