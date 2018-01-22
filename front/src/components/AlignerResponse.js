import React, { Component } from 'react'
import { graphql } from 'react-apollo'
import gql from 'graphql-tag'
import { Form, Message } from 'semantic-ui-react'

class AlignerResponse extends Component {

  render() {
    const bitextsToRender = this.props.allDataQuery.bitexts
    const CategoriesToRender = this.props.allDataQuery.allCategories

    console.log(bitextsToRender)
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
          {bitextsToRender.map(bitext => (
            <li key={bitext.id}> Bitext #{bitext.id} :
              <p>{bitext.french}</p>
              <p>{bitext.english}</p>
            </li>
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
    bitexts {
      id
      french
      english
    }
  }
`

export default graphql(ALL_DATA, {
  name: 'allDataQuery',
  options: { pollInterval: 5000 }
}) (AlignerResponse)
