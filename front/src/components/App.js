import React, { Component } from 'react'
import { Switch, Route } from 'react-router-dom'
import Header from './Header.js'
import Homepage from './Homepage.js'
import Aligner from './Aligner.js'
import '../styles/App.css'

class App extends Component {
  render() {
    return (
      <div className='App'>
        <Header />
        <div className='ph3 pv1 background-gray'>
          <Switch>
            <Route exact path='/' component={Homepage}/>
            <Route exact path='/aligner' component={Aligner}/>
          </Switch>
        </div>
      </div>
    );
  }
}

export default App
