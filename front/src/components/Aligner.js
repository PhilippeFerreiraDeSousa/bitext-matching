import React, { Component } from 'react'
import ResponseProgress from './ResponseProgress'
import AlignerForm from './AlignerForm'

class Aligner extends Component {
  constructor() {
    super();
    this.state = {
      bitextId: null,
    }
  }

  setBitextId = (id) => {
    this.setState(({bitextId}) => ({
      bitextId: id
    }))
  }

  render() {
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
