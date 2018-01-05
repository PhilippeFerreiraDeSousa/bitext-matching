import React, { Component } from 'react'
import { Switch, Route } from 'react-router-dom'
import Header from './Header'
import Homepage from './Homepage'
import Aligner from './Aligner'
import NotFound from './NotFound'
import { Container } from 'semantic-ui-react'
import '../styles/css/App.css'

class App extends Component {
  render() {
    return (
      <div className='App'>
        <Header />
        <Container className='App-body' text>
          <Switch>
            <Route exact path='/' component={Homepage}/>
            <Route exact path='/aligner' component={Aligner}/>
            <Route path="*" component={NotFound} />
          </Switch>
        </Container>
      </div>
    );
  }
}

export default App
