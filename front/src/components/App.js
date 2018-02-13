import React, { Component } from 'react'
import { Switch, Route, Redirect } from 'react-router-dom'
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
          <Redirect exact from='/' to='/home'/>
          <Route exact path='/home' component={Homepage}/>
          <Route path='/' component={AppMenu}/>
          <Route path="*" component={NotFound} />
        </Switch>
      </div>
    );
  }
}

export default App
