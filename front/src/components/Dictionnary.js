import React, { Component } from 'react'
import { graphql } from 'react-apollo'
import gql from 'graphql-tag'
import { Dropdown } from 'semantic-ui-react'
import WordList from './WordList'

class Dictionnary extends Component {
  state = {
    wordId: null
  }

  handleInputChange = (event, { name, value }) => {
    this.setState({
        [name]: value
    });
  }

  render() {
    const wordsToRender = this.props.wordQuery.allWords
    var wordOptions =  []

    console.log(wordsToRender)

    if (this.props.wordQuery && this.props.wordQuery.error) {
      return <div>Error</div>
    }
    if (this.props.wordQuery && !this.props.wordQuery.loading) {
      wordOptions = wordsToRender.map(word => ({key: word.id, value: word.id, text: word.content+" ("+word.language.substring(0, 2)+")"}) )
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
  options: { pollInterval: 5000 }
}) (Dictionnary)