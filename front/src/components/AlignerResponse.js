import React, { Component } from 'react'
import { graphql } from 'react-apollo'
import gql from 'graphql-tag'
import { Form, Message } from 'semantic-ui-react'

class AlignerResponse extends Component {

  render() {
    const linksToRender = this.props.allDataQuery.links
    const CategoriesToRender = this.props.allDataQuery.allCategories

    console.log(linksToRender)
    console.log(CategoriesToRender)

    if (this.props.allDataQuery && this.props.allDataQuery.loading) {
      return <div>Loading</div>
    }
    if (this.props.allDataQuery && this.props.allDataQuery.error) {
      return <div>Error</div>
    }
    return(
      <div>
        <ul>
          {linksToRender.map(link => (
            <li key={link.id}><a href={link.url}>{link.description}</a></li>
          ))}
        </ul>
        {CategoriesToRender.map(category => (
          <ul key={category.id}>
            <li>
              Catégorie {category.id} <br />
              Nom : {category.name} <br />
              Ingrédients :
              <ul>
              {category.ingredients.map(ingredient => (
                <li key={ingredient.id}>{ingredient.name}</li>
              ))}
              </ul>
            </li>
          </ul>
        ))}
      </div>
    );
  }
}

const ALL_DATA = gql`
  query allData {
    allCategories {
      id
      name
      ingredients {
        id
        name
      }
    }
    links {
      id
      description
      url
    }
  }
`

export default graphql(ALL_DATA, { name: 'allDataQuery' }) (AlignerResponse)
