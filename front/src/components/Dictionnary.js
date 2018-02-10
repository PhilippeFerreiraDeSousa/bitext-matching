import React, { Component } from 'react'
import { graphql } from 'react-apollo'
import gql from 'graphql-tag'
import { Dropdown, Flag } from 'semantic-ui-react'
import WordList from './WordList'
import { flags } from '../parameters/flags'
import ErrorMessage from './ErrorMessage'

class Dictionnary extends Component {
  state = {
    wordId: null
  }

  handleInputChange = (event, { value }) => {
    this.setState({
        wordId: value.id
    })
  }

  render() {
    const wordsToRender = this.props.wordQuery.allWords
    var wordOptions =  []

    console.log(wordsToRender)
    console.log(this.state)

    if (this.props.wordQuery && this.props.wordQuery.error) {
      return <ErrorMessage />
    }
    if (this.props.wordQuery && !this.props.wordQuery.loading) {
      wordOptions = wordsToRender.map(word => ({key: word.id, value: word, flag: flags[word.language], text: word.content }))
    }

    return(
      <div>
        <Dropdown placeholder='Select word' fluid search selection options={wordOptions} onChange={this.handleInputChange} loading={this.props.wordQuery && this.props.wordQuery.loading} />
        { this.state.wordId ? <WordList wordId={this.state.wordId} /> : null }
      </div>
    );
  }
}

const WORDS = gql`
  query words {
    allWords {
      id
      language
      content
  	}
  }
`

export default graphql(WORDS, {
  name: 'wordQuery',
  //options: { pollInterval: 5000 }
}) (Dictionnary)
