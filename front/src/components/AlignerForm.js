import React, { Component } from 'react'
import { graphql } from 'react-apollo'
import gql from 'graphql-tag'
import { Form, Message } from 'semantic-ui-react'
import { Map } from 'immutable'

class AlignerForm extends Component {
  constructor() {
    super();
    this.state = {
      data: Map({
        title: '',
        author: '',
        french: '',
        english: ''
      }),
      status: Map({
        loading: false
      })
    }
  }

  submitBitext = () => {
    const french = this.state.data.get('french')
    const english = this.state.data.get('english')
    const title = this.state.data.get('title')
    const author = this.state.data.get('author')
    this.props.submitBitextMutation({
      variables: {
        french,
        english,
        title,
        author
      }
    })
    .then(({ data }) => {
      this.props.set_bitext(data.submitBitext.id)
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
            <Form.TextArea label='French text' field='french' required value={data.get('french')} placeholder='Il était une fois...' onChange={this.handleChange}/>
            <Form.TextArea label='English text' field='english' required value={data.get('english')} placeholder='Once upon a time...' onChange={this.handleChange}/>
          </Form.Group>
          <Form.Button primary>Send</Form.Button>
        </Form>
      </div>
    );
  }
}

const SUBMIT_BITEXT_MUTATION = gql`
  mutation SubmitBitextMutation($french: String!, $english: String!, $title: String!, $author: String!) {
    submitBitext(
      french: $french,
      english: $english,
      title: $title,
      author: $author
    ) {
      id
    }
  }
`

export default graphql(SUBMIT_BITEXT_MUTATION, { name: 'submitBitextMutation' })(AlignerForm)
