import React, { Component } from 'react'
import AlignerForm from './AlignerForm'
import AlignerResponse from './AlignerResponse'
import BitextData from './BitextData'

class Aligner extends Component {
  constructor() {
    super();
    this.state = {
      bitextId: null,
      language: null
    }
  }

  set_bitext = (id, lang) => {
    this.setState({
      bitextId: id,
      language: lang
    })
    console.log(id)
  }

  render() {
    console.log(this.state)
    return(
      <div>
        <AlignerForm set_bitext={this.set_bitext}/>
        <br />
        { this.state.bitextId ? <BitextData bitextId={this.state.bitextId} language={this.state.language} /> : null }
      </div>
    )
  }
}

export default Aligner
