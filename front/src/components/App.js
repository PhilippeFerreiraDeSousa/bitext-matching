import React, { Component } from 'react'
import { Switch, Route } from 'react-router-dom'
import Header from './Header'
import Homepage from './Homepage'
import Aligner from './Aligner'
import NotFound from './NotFound'
import '../styles/App.css'

class App extends Component {
  render() {
    return (
      <div className='App'>
        <Header />
        <div>
          <Switch>
            <Route exact path='/' component={Homepage}/>
            <Route exact path='/aligner' component={Aligner}/>
            <Route path="*" component={NotFound} />
          </Switch>
        </div>
      </div>
    );
  }
}

export default App
