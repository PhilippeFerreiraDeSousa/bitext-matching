import React, { Component } from 'react'
import { graphql } from 'react-apollo'
import gql from 'graphql-tag'
import { Form, Message } from 'semantic-ui-react'
import { Map } from 'immutable'
import BitextData from './BitextData'

const languageOptions = [
  {
    key: 0,
    value: 'english',
    text: 'English'
  },
  {
    key: 1,
    value: 'french',
    text: 'Français'
  },
  {
    key: 2,
    value: 'russian',
    text: 'Russian'
  },
  {
    key: 3,
    value: 'spanish',
    text: 'Spanish'
  },
  {
    key: 4,
    value: 'german',
    text: 'German'
  },
  {
    key: 5,
    value: 'portuguese',
    text: 'Portuguese'
  },
  {
    key: 6,
    value: 'italian',
    text: 'Italian'
  }
]

class AlignerForm extends Component {
  constructor() {
    super();
    this.state = {
      data: Map({
        bitextId: null,
        text1: '',
        text2: '',
        language1: '',
        language2: '',
        title: '',
        author: ''
      }),
      status: Map({
        loading: false
      })
    }
  }

  submitBitext = () => {
    const text1 = this.state.data.get('text1')
    const text2 = this.state.data.get('text2')
    const language1 = this.state.data.get('language1')
    const language2 = this.state.data.get('language2')
    const title = this.state.data.get('title')
    const author = this.state.data.get('author')
    this.props.submitBitextMutation({
      variables: {
        text1,
        text2,
        language1,
        language2,
        title,
        author
      }
    })
    .then(({ data }) => {
      this.setState({
        data: data.update('bitextId', () => data.submitBitext.id)
      })
    }).catch((error) => {
      console.log('there was an error sending the query', error)
    });
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
    this.setState(({data}) => ({
      data: data.update(field, () => value)
    }))
  }

  render() {
    const data = this.state.data
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
        >
          <Form.Group widths='equal'>
            <Form.Input label='Title' placeholder='Le Petit Prince' required field='author' value={data.get('name')} onChange={this.handleChange}/>
            <Form.Input label='Author' placeholder='Antoine de Saint-Exupéry' field="author" value={data.get('name')} onChange={this.handleChange}/>
          </Form.Group>
          <Form.Group widths='equal' onSubmit={this.handleSubmit}>
            <Form.TextArea label='First text' field='text1' required value={data.get('text1')} placeholder='Il était une fois...' onChange={this.handleChange}/>
            <Form.TextArea label='Second text' field='text2' required value={data.get('text2')} placeholder='Once upon a time...' onChange={this.handleChange}/>
          </Form.Group>
          <Form.Group widths='equal'>
            <Form.Dropdown placeholder='Select language' field='language1' required search selection options={languageOptions} onChange={this.handleChange} />
            <Form.Dropdown placeholder='Select language' field='language2' required search selection options={languageOptions} onChange={this.handleChange} />
          </Form.Group>
          <Form.Button primary>Send</Form.Button>
        </Form>
        <br />
        { data.get('bitextId') ? <BitextData bitextId={data.get('bitextId')} language1={data.get('language1')} language2={data.get('language2')} /> : null }
      </div>
    );
  }
}

const SUBMIT_BITEXT_MUTATION = gql`
  mutation SubmitBitextMutation($text1: String!, $text2: String!, $language1: String!, $language2: String!, $title: String!, $author: String!) {
    submitBitext(
      text1: $text1,
      text2: $text2,
      language1: $language1,
      language2: $language2,
      title: $title,
      author: $author
    ) {
      id
    }
  }
`

export default graphql(SUBMIT_BITEXT_MUTATION, { name: 'submitBitextMutation' })(AlignerForm)
