import React, { Component } from 'react'
import { graphql, compose } from 'react-apollo'
import gql from 'graphql-tag'
import { Form, Message } from 'semantic-ui-react'
import { Map } from 'immutable'
import ResponseProgress from './ResponseProgress'
import { languageOptions } from '../parameters/flags'
import { SendingErrorMessage } from './ErrorMessage'

class AlignerForm extends Component {
  constructor() {
    super();
    this.state = {
      info: Map({
        bitextId: null,
        text1: '',
        text2: '',
        language1: '',
        language2: '',
        title: '',
        author: ''
      }),
      status: Map({
        loading: false,
        error: false
      })
    }
  }

  alignBitext = (id) => {
    const text1 = this.state.info.get('text1')
    const text2 = this.state.info.get('text2')
    const language1 = this.state.info.get('language1')
    const language2 = this.state.info.get('language2')
    this.props.alignBitextMutation({
      variables: {
        id,
        text1,
        text2,
        language1,
        language2
      }
    })
    .then(({ data }) => {
      this.setState(({info, status}) => ({
        status: status.update('error', () => false)
      }))
    }).catch((error) => {
      this.setState(({status}) => ({
        status: status.update('error', () => true)
      }))
    })
  }

  submitBitext = () => {
    const title = this.state.info.get('title')
    const author = this.state.info.get('author')
    this.props.submitBitextMutation({
      variables: {
        title,
        author
      }
    })
    .then(({ data }) => {
      this.setState(({info, status}) => ({
        info: info.update('bitextId', () => data.submitBitext.id),
        status: status.update('error', () => false)
      }))
      this.alignBitext(data.submitBitext.id)
    }).catch((error) => {
      this.setState(({status}) => ({
        status: status.update('error', () => true)
      }))
    })
  }

  handleSubmit = async () => {
    this.setState(({status}) => ({
      status: status.update('loading', () => true)
    }))
    await this.submitBitext()
    this.setState(({status}) => ({
      status: status.update('loading', () => false)
    }))
  }

  handleChange = (e, { field, value }) => {
    this.setState(({info}) => ({
      info: info.update(field, () => value)
    }))
  }

  render() {
    const info = this.state.info
    const status = this.state.status

    return(
      <div>
        <Message
            header="Let's align bitexts !"
            attached='top'
        />
        <Form
          className='fluid segment attached'
          onSubmit={this.handleSubmit}
          loading={status.get('loading')}
          error={status.get('error')}
        >
          <Form.Group widths='equal'>
            <Form.Input label='Title' placeholder='Le Petit Prince' required field='title' value={info.get('title')} onChange={this.handleChange}/>
            <Form.Input label='Author' placeholder='Antoine de Saint-Exupéry' field="author" value={info.get('author')} onChange={this.handleChange}/>
          </Form.Group>
          <Form.Group widths='equal' onSubmit={this.handleSubmit}>
            <Form.TextArea label='First text' field='text1' required value={info.get('text1')} placeholder='Il était une fois...' onChange={this.handleChange}/>
            <Form.TextArea label='Second text' field='text2' required value={info.get('text2')} placeholder='Once upon a time...' onChange={this.handleChange}/>
          </Form.Group>
          <Form.Group widths='equal'>
            <Form.Dropdown placeholder='Select language' field='language1' required search selection options={languageOptions} onChange={this.handleChange} />
            <Form.Dropdown placeholder='Select language' field='language2' required search selection options={languageOptions} onChange={this.handleChange} />
          </Form.Group>
          <Form.Button primary>Send</Form.Button>
          <SendingErrorMessage />
        </Form>
        <br />
        { info.get('bitextId') ? <ResponseProgress bitextId={info.get('bitextId')} /> : null }
      </div>
    );
  }
}

const SUBMIT_BITEXT_MUTATION = gql`
  mutation SubmitBitextMutation($title: String!, $author: String!) {
    submitBitext(
      title: $title,
      author: $author
    ) {
      id
    }
  }`

  const ALIGN_BITEXT_MUTATION = gql`
    mutation alignBitextMutation($id: Int!, $text1: String!, $text2: String!, $language1: String!, $language2: String!) {
      alignBitext(
        id: $id
        text1: $text1,
        text2: $text2,
        language1: $language1,
        language2: $language2,
      ) {
        id
      }
    }
`

export default compose(
  graphql(SUBMIT_BITEXT_MUTATION, {
    name: 'submitBitextMutation'
  }),
  graphql(ALIGN_BITEXT_MUTATION, {
    name: 'alignBitextMutation'
  })
)(AlignerForm)
