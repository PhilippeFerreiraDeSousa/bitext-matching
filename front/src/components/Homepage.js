import React, { Component } from 'react'
import { Container } from 'semantic-ui-react'

class Homepage extends Component {
  render() {
    return(
      <Container className='App-body' text>
        <section>
          <h2>What is bitext alignment ?</h2>
          <p>
            Bitext alignment consists in aligning to texts written in two different
            languages assumed to be transolations of one another. The goal is to match
            paragraphs and sentences. It is mainly used my translators across the
            world to produce more accurate traductions taking into account the context
            and the more commonly used expressions of a language.
          </p>
          <p>
            This site is in conctruction please find more advanced projects here :
          </p>
          <ul>
            <li><a href='https://elizia.net/alignator/alignator.cgi'>Elizia&#39;s alignator</a></li>
            <li><a href='http://miaojun.net/alignoscope/'>Miaojun&#39;s alignoscope</a></li>
          </ul>
          <a href='https://github.com/PhilippeFerreiraDeSousa/bitext-matching' target='_blank' rel='noopener noreferrer'
          className='ui button'><i className='github icon'></i>Visit our dev Repo</a>
        </section>
      </Container>
    );
  }
}

export default Homepage
