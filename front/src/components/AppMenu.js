import React, { Component } from 'react'
import { Container, Menu } from 'semantic-ui-react'
import Aligner from './Aligner'
import AlignedBitext from './AlignedBitext'
import Dictionnary from './Dictionnary'
import { Switch, Route, Link } from 'react-router-dom'

class AppMenu extends Component {
  render() {
    const activeItem = this.props.location.pathname.slice(1)

    return (
      <Container className='App-body'>
        <Menu>
          <Menu.Item
            active={activeItem === 'form'}
            as={Link}
            to='/form'
          >
            <i className='tasks icon'></i>Aligner
          </Menu.Item>

          <Menu.Item
            active={activeItem === 'archive'}
            as={Link}
            to='/archive'
          >
            <i className='unhide icon'></i>Aligned bitexts
          </Menu.Item>

          <Menu.Item
            active={activeItem === 'dictionnary'}
            as={Link}
            to='/dictionnary'
          >
            <i className='translate icon'></i>Translate
          </Menu.Item>
        </Menu>
        <Switch>
          <Route exact path="/form" component={Aligner} />
          <Route exact path="/archive" component={AlignedBitext} />
          <Route exact path="/dictionnary" component={Dictionnary} />
        </Switch>
      </Container>
    )
  }
}

export default AppMenu
