import React, { Component } from 'react'
import AlignerForm from './AlignerForm'
import AlignerResponse from './AlignerResponse'
import { Container } from 'semantic-ui-react'

class Aligner extends Component {
  constructor() {
    super();
    this.state = {
      bitextId: null
    }
  }
  set_bitext(id) {
    this.setState({
      bitextId: id
    })
    console.log(id)
  }

  render() {
    return(
      <Container className='App-body'>
        <AlignerForm set_bitext={this.set_bitext}/>
        <br />
        { this.state.bitextId ? <AlignerResponse bitextId={this.state.bitextId} /> : null }
      </Container>
    );
  }
}

export default Aligner
