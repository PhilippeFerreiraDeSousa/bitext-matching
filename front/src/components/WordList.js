import React, { Component } from 'react'
import { graphql } from 'react-apollo'
import gql from 'graphql-tag'
import { Grid, Segment, List, Flag, Loader } from 'semantic-ui-react'
import flags from '../parameters/flags'
import ErrorMessage from './ErrorMessage'

var groupByLanguage = function(xs, wordId) {
  return xs.reduce(function(rv, x) {
    if (x.word1.id === wordId ) {
      var translationWord = 'word2'
      var translatedWord = 'word1'
      var translationSentence = 'sentence2'
      var translatedSentence = 'sentence1'
    } else {
      var translationWord = 'word1'
      var translatedWord = 'word2'
      var translationSentence = 'sentence1'
      var translatedSentence = 'sentence2'
    }
    (rv[x[translationWord]['content']] = rv[x[translationWord]['content']] || [])
    .push({ id: x.id, bitext: x.bitext, translationLanguage: x[translationWord].language, translatedSentence: x[translatedSentence], translationSentence: x[translationSentence]})
    return rv
  }, {})
}

class WordList extends Component {

  render() {
    const translationsToRender = this.props.translationQuery.translations
    const wordId = this.props.wordId

    console.log(translationsToRender)

    if (this.props.translationQuery && this.props.translationQuery.loading) {
      return <Loader active inline='centered' />
    }
    if (this.props.translationQuery && this.props.translationQuery.error) {
      return <ErrorMessage />
    }
    const wordList = groupByLanguage(translationsToRender, wordId)

    return(
      <List>
        { Object.keys(wordList).map((word, idx) => (
          <List.Item key={idx} >
            <List.Content>
              <List.Header><Flag name={flags[wordList[word][0].translationLanguage]} />{word}</List.Header>
            </List.Content>
            <List.List>
              {wordList[word].map( translation => (
                <List.Item key={translation.id}>
                  <List.Icon name='book' />
                  <List.Content>
                    <List.Header>{translation.bitext.title}</List.Header>
                    <List.Description style={{font: 'caption'}}>{translation.bitext.author}</List.Description>
                  </List.Content>
                  <Grid columns={2} divided='vertically'>
                    <Grid.Row>
                      <Grid.Column>
                        <Segment>
                          {translation.translatedSentence.content}
                        </Segment>
                      </Grid.Column>
                      <Grid.Column>
                        <Segment>
                          {translation.translationSentence.content}
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
        id
        content
        language
      }
      word2 {
        id
        content
        language
      }
      sentence1 {
        content
      }
      sentence2 {
        content
      }
  	}
  }
`

export default graphql(TRANSLATIONS, {
  name: 'translationQuery',
  options: ({ wordId }) => ({
    variables: { wordId: wordId }
  })
}) (WordList)
