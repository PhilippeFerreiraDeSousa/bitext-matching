import React, { Component } from 'react'
import AlignerForm from './AlignerForm'
import AlignerResponse from './AlignerResponse'

class Aligner extends Component {
  constructor() {
    super();
    this.state = {
      bitextId: null,
    }
  }

  set_bitext = (id) => {
    this.setState({
      bitextId: id
    })
    console.log(id)
  }

  render() {
    console.log(this.state)
    return(
      <div>
        <AlignerForm set_bitext={this.set_bitext}/>
        <br />
        { this.state.bitextId ? <AlignerResponse bitextId={this.state.bitextId} /> : null }
      </div>
    )
  }
}

export default Aligner
