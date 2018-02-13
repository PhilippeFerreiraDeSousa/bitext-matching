import React, { Component } from 'react'
import { Link } from 'react-router-dom'
import { withRouter } from 'react-router'

class Header extends Component {
  render() {
    return(
      <header className='App-header'>
        <Link to='/home'><img src='../img/logo.png' className='App-logo' alt='logo' /></Link>
        <Link to='/form'><h1 className='App-title'>ENPC bitext aligner</h1></Link>
      </header>
    );
  }
}

export default withRouter(Header)
