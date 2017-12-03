import React, { Component } from 'react'
import { graphql } from 'react-apollo'
import gql from 'graphql-tag'

class Aligner extends Component {
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
      <section className='App-body'>
        <h2>Let&#39;s align bitexts !</h2>
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
      </section>
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

export default graphql(ALL_DATA, { name: 'allDataQuery' }) (Aligner)
