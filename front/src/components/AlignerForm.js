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
        french: '',
        english: ''
      }),
      status: Map({
        loading: false
      })
    }
  }

  createLink = () => {
    const description = this.state.data.get('french')
    const url = this.state.data.get('english')
    this.props.createLinkMutation({
      variables: {
        description,
        url
      }
    })
  }

  handleSubmit = async () => {
    this.setState(({status}) => ({
      status: status.update('loading', () => true)
    }))
    await this.createLink()
    this.setState(({status}) => ({
      status: status.update('loading', () => false)
    }))
    console.log(this.state)
  }

  handleChange = (e, { language, value }) => {
    this.setState(({data}) => ({
      data: data.update(language, () => value)
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
          <Form.Group widths='equal' onSubmit={this.handleSubmit}>
            <Form.TextArea label='French text' language='french' value={data.get('french')} placeholder='Il était une fois...' onChange={this.handleChange}/>
            <Form.TextArea label='English text' language='english' value={data.get('english')} placeholder='Once upon a time...' onChange={this.handleChange}/>
          </Form.Group>
          <Form.Button primary>Envoyer</Form.Button>
        </Form>
      </div>
    );
  }
}

const CREATE_LINK_MUTATION = gql`
  mutation CreateLinkMutation($description: String!, $url: String!) {
    createLink(
      description: $description,
      url: $url,
    ) {
      id
      url
      description
    }
  }
`

export default graphql(CREATE_LINK_MUTATION, { name: 'createLinkMutation' })(AlignerForm)
