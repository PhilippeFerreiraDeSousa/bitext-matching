import React, { Component } from 'react'
import { Switch, Route } from 'react-router-dom'
import Header from './Header'
import Homepage from './Homepage'
import AppMenu from './AppMenu'
import NotFound from './NotFound'
import '../styles/css/App.css'

class App extends Component {
  render() {
    return (
      <div className='App'>
        <Header />
        <Switch>
          <Route exact path='/' component={Homepage}/>
          <Route exact path='/aligner' component={AppMenu}/>
          <Route path="*" component={NotFound} />
        </Switch>
      </div>
    );
  }
}

export default App
