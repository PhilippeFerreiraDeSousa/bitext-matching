import React, { Component } from 'react'
import { Container, Menu } from 'semantic-ui-react'
import AlignerForm from './AlignerForm'
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
            <i className='tasks icon'></i>Aligner
          </Menu.Item>

          <Menu.Item
            name='aligned'
            active={activeItem === 'aligned'}
            onClick={this.handleItemClick}
          >
            <i className='unhide icon'></i>Aligned bitexts
          </Menu.Item>

          <Menu.Item
            name='dictionnary'
            active={activeItem === 'dictionnary'}
            onClick={this.handleItemClick}
          >
            <i className='translate icon'></i>Translate
          </Menu.Item>
        </Menu>
        {   this.state.activeItem === 'aligner' ? (
          <AlignerForm />
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
