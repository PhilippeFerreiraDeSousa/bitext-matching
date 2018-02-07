import React, { Component } from 'react'
import { graphql } from 'react-apollo'
import gql from 'graphql-tag'
import { Grid, Segment } from 'semantic-ui-react'

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
    return(
      <ul>
        { translationsToRender.map( translation => (
          <li key={translation.id}>
            <p>{language === 'english' ? translation.word2.content : translation.word1.content }</p>
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
          </li>
        ))}
      </ul>
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
