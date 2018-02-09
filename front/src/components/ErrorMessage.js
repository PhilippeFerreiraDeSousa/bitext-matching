import React from 'react'
import { Message } from 'semantic-ui-react'

const ErrorMessage = () => (
  <Message negative>
    <Message.Header>We&#39;re sorry an error has occured</Message.Header>
    <p>Problem fetching data...</p>
  </Message>
)

export default ErrorMessage
