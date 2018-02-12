import React, { Component } from 'react'
import { graphql, compose } from 'react-apollo'
import gql from 'graphql-tag'
import { Form, Message } from 'semantic-ui-react'
import { Map } from 'immutable'
import ResponseProgress from './ResponseProgress'
import AlignerForm from './AlignerForm'
import { languageOptions } from '../parameters/flags'
import { SendingErrorMessage } from './ErrorMessage'

class Aligner extends Component {
  constructor() {
    super();
    this.state = {
      bitextId: null,
    }
  }

  setBitextId = (id) => {
    console.log("coucou")
    console.log(id)
    this.setState(({bitextId}) => ({
      bitextId: id
    }))
    console.log(this.state.bitextId)
  }

  render() {
    console.log(this.state.bitextId)

    return(
      <div>
        <AlignerForm setBitextId={this.setBitextId}/>
        <br />
        { this.state.bitextId ? <ResponseProgress bitextId={this.state.bitextId} /> : null }
      </div>
    )
  }
}

export default Aligner
