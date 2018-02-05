import React, { Component } from 'react'
import AlignerForm from './AlignerForm'
import AlignerResponse from './AlignerResponse'
import { Container } from 'semantic-ui-react'

class Aligner extends Component {

  render() {
    return(
      <Container className='App-body'>
        <AlignerForm />
        <br />
        <AlignerResponse />
      </Container>
    );
  }
}

export default Aligner
