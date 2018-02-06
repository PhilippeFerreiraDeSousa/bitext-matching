import React, { Component } from 'react'
import { Container, Menu } from 'semantic-ui-react'
import Aligner from './Aligner'
import AlignedBitext from './AlignedBitext'
import Dictionnary from './Dictionnary'

class AppMenu extends Component {
  state = { activeItem: 'aligner' }

  handleItemClick = (e, { name }) => {
    this.setState({ activeItem: name })
  }

  render() {
    const { activeItem } = this.state

    return (
      <Container className='App-body'>
        <Menu>
          <Menu.Item
            name='aligner'
            active={activeItem === 'aligner'}
            onClick={this.handleItemClick}
          >
            Aligneur
          </Menu.Item>

          <Menu.Item
            name='aligned'
            active={activeItem === 'aligned'}
            onClick={this.handleItemClick}
          >
            Bitextes alignés
          </Menu.Item>

          <Menu.Item
            name='dictionnary'
            active={activeItem === 'dictionnary'}
            onClick={this.handleItemClick}
          >
            Dictionnaire
          </Menu.Item>
        </Menu>
        {   this.state.activeItem === 'aligner' ? (
          <Aligner />
        ) : this.state.activeItem === 'aligned' ? (
          <AlignedBitext />
        ) : this.state.activeItem === 'dictionnary' ? (
          <Dictionnary />
        ) : null }
      </Container>
    )
  }
}

export default AppMenu
