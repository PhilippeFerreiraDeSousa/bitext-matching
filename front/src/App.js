import React, { Component } from 'react';
import logo from './logo.svg';
import './App.css';

class App extends Component {
  render() {
    return (
      <div className="App">
        <header className="App-header">
          <img src={logo} className="App-logo" alt="logo" />
          <h1 className="App-title">Welcome to our project</h1>
        </header>
        <section className="App-body">
          <h2>What is bitext alignment ?</h2>
          <p className="App-intro">
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
            <li><a href="https://elizia.net/alignator/alignator.cgi">Elizia&#39;s alignator</a></li>
            <li><a href="http://miaojun.net/alignoscope/">Miaojun&#39;s alignoscope</a></li>
          </ul>
        </section>
      </div>
    );
  }
}

export default App;
