import React, { Component } from 'react'
import AlignerForm from './AlignerForm'
import AlignerResponse from './AlignerResponse'

class Aligner extends Component {

  render() {
    return(
      <div>
        <AlignerForm />
        <br />
        <AlignerResponse />
      </div>
    );
  }
}

export default Aligner
