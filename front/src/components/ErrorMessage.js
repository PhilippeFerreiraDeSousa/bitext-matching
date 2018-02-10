import React from 'react'
import { Message } from 'semantic-ui-react'

const FetchingErrorMessage = () => (
  <Message negative>
    <Message.Header>We&#39;re sorry an error has occured</Message.Header>
    <p>Problem fetching data...</p>
  </Message>
)

const SendingErrorMessage = () => (
  <Message error >
    <Message.Header>We&#39;re sorry an error has occured</Message.Header>
    <p>Problem sending data</p>
  </Message>
)

export { FetchingErrorMessage, SendingErrorMessage }
