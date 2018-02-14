import React, { Component } from 'react'
import { Link } from 'react-router-dom'
import { Container, Button, Icon } from 'semantic-ui-react'

class Homepage extends Component {
  render() {
    return(
      <Container className='App-body' text>
        <section>
          <h2>What is bitext alignment ?</h2>
          <p>
            Bitext alignment consists in aligning two texts written in two different
            languages assumed to be translations of one another. The goal is to match
            paragraphs and sentences. It is mainly used my translators across the
            world to produce more accurate translations taking into account the context
            and the more commonly used expressions of a language.
          </p>
          <Link to='/form'>
            <Button primary align='center'>
              <Icon name='tasks'></Icon>
              Let&#39;s get started !
            </Button>
          </Link>
          <h2>About the project</h2>
          <p>
            This is an opensource project started by a group of students at the Ecole des Ponts engineering school.
            You can read about the theory behind our alignment algorithms <a href='theory.pdf' target='_blank' rel='noopener noreferrer'>here</a>.
          </p>
          <Button primary href='https://github.com/PhilippeFerreiraDeSousa/bitext-matching' target='_blank' rel='noopener noreferrer'>
            <Icon name='github'></Icon>
            Visit our dev Repo
          </Button>
        </section>
      </Container>
    );
  }
}

export default Homepage
