import React, { Component } from 'react'
import { Link } from 'react-router-dom'
import { withRouter } from 'react-router'
import logo from './logo.svg'

class Header extends Component {
  render() {
    return(
      <header className='App-header'>
        <Link to='/'><img src={logo} className='App-logo' alt='logo' /></Link>
        <Link to='/aligner'><h1 className='App-title'>Welcome to our project</h1></Link>
      </header>
    );
  }
}

export default withRouter(Header)
