import React, { Component } from 'react'
import '../styles/css/NotFound.css'
class NotFound extends Component {
  render () {
    return (
      <div className='NotFound'>
        <img src='/img/error-404.svg' className='NotFound__image'/>
      </div>
    )
  }
}

export default NotFound
