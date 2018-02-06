import React, { Component } from 'react'
import { graphql } from 'react-apollo'
import gql from 'graphql-tag'
import {  } from 'semantic-ui-react'

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
        { translationsToRender.map( translation => (<li key={translation.id}>{language === 'english' ? translation.word2.content : translation.word1.content }</li>) ) }
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
        sentences {
          id
          content
        }
      }
      word2 {
        content
        sentences {
          id
          content
        }
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
