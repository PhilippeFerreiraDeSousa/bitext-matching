# Bitext-matching
Mise en correspondance de bitextes dans des langues différentes

## Support ressources
- Html : https://www.w3schools.com/html/
- CSS : https://www.w3schools.com/css/
- Javascript : https://openclassrooms.com/courses/dynamisez-vos-sites-web-avec-javascript
- Yarn : https://yarnpkg.com

- Reactjs :
  - https://openclassrooms.com/courses/build-web-apps-with-reactjs
  - https://reactjs.org/tutorial/tutorial.html
  - React-redux : https://redux.js.org/docs/basics/UsageWithReact.html
  - Semantic UI React : https://react.semantic-ui.com/usage
  - Apollo Link : https://www.apollographql.com/docs/link/#apollo-client
    The HttpLink is a replacement for createNetworkInterface from Apollo Client 1.0

- GraphQL :
  - http://graphql.org
  - https://www.howtographql.com

- Python : https://openclassrooms.com/courses/apprenez-a-programmer-en-python
- Ctypes : https://docs.python.org/3/library/ctypes.html
- Django : https://www.djangoproject.com
  - Graphene-Django : http://docs.graphene-python.org/projects/django/en/latest/
  - Pytest-django : https://pytest-django.readthedocs.io/en/latest/
  - Django-cors-headers : https://github.com/ottoyiu/django-cors-headers

Extra ressources :
- https://github.com/mbrochh/django-graphql-apollo-react-demo
- https://dev-blog.apollodata.com/full-stack-react-graphql-tutorial-582ac8d24e3b
- CORS : https://fr.wikipedia.org/wiki/Cross-origin_resource_sharing
- React-redux creator workflow : https://www.youtube.com/watch?v=xsSnOQynTHs
- GraphQL at Facebook :
  - https://dev-blog.apollodata.com/graphql-at-facebook-by-dan-schafer-38d65ef075af
  - React 16 Fiber : https://www.youtube.com/watch?v=QW5TE4vrklU

## Install
Sous Debian ou dérivé, exécutez `./install-debian.sh`

## Test

Pour voir le rapport de couverture, faire
```
cd back/
pytest --cov-report html --cov
```
Puis ouvrir htmlcov/index.html dans un navigateur.

Pour exécuter les tests:
```
cd back/
pytest
```

## GraphiQL playground

Run the Django web server :
```
cd back/
python manage.py runserver
```
Go to http://localhost:8000/graphiql and query for
```
{
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
```
Click on "docs" on the right-hand corner to go through the graph structure.

## Admin pannel

Run the Django web server and create an admin account :
```
cd back/
python manage.py createsuperuser
python manage.py runserver
```
Go to http://localhost:8000/admin

## [Query Batching](https://www.apollographql.com/docs/react/basics/network-layer.html)

Apollo lets you automatically batch multiple queries into one request when they are made within a certain interval. This means that if you render several components, for example a navbar, sidebar, and content, and each of those do their own GraphQL query, they will all be sent in one roundtrip. Batching works only with server that support batched queries (for example graphql-server). Batched requests to servers that don’t support batching will fail. To learn how to use batching with Apollo checkout the [indepth guide](https://www.apollographql.com/docs/link/links/batch-http.html)

## [Mixer for Django's ORM](http://mixer.readthedocs.io/en/latest/quickstart.html)

```
from mixer.backend.django import mixer

# Generate model with some values
client = mixer.blend(Client, username='test')
assert client.username == 'test'

# Generate model with reference
message = mixer.blend(Message, client__username='test2')
assert message.client.username == 'test2'

# Value may be callable
client = mixer.blend(Client, username=lambda:'callable_value')
assert client.username == 'callable_value'

# Value may be a generator
clients = mixer.cycle(4).blend(Client, username=(name for name in ('Piter', 'John')))

# Value could be getting a counter
clients = mixer.cycle(4).blend(Client, username=mixer.sequence(lambda c: "test_%s" % c))
print clients[2].username  # --> 'test_2'

# Short format for string formating
clients = mixer.cycle(4).blend(Client, username=mixer.sequence("test_{0}"))
print clients[2].username  # --> 'test_2'

# Force to generation of a default (or null) values
client = mixer.blend(Client, score=mixer.RANDOM)
print client.score  # Some like: --> 456

# Set related values from db by random
message = mixer.blend(Message, client=mixer.SELECT)
assert message.client in Client.objects.all()
```

## [Lazy loading routes](https://scotch.io/tutorials/lazy-loading-routes-in-react) : or use *react-loadable* instead

In React, we can lazy load components and routes by code splitting using Webpack. By splitting our app into chunks we can load & evaluate only the code that is required for the page rendered.
A React app has routes/components that can use several React plugins. Without code splitting, all the React code and plugins in use will be bundled into one JavaScript file, but with code splitting, only the component/plugin needed would be loaded.

## Alignment algorithms

### Dynamic Text Wrapping

### IBM Model 2

### Algo Victoriya

## Run optimized version for production

Execute
```
yarn global add serve

cd back/
python manage.py runserver

cd ../front/
yarn build
serve -s build
```
Go to http://localhost:3000

## Images
- Error page : https://pixabay.com/en/error-404-page-was-not-found-news-1349562/

## TODO :
- https://github.com/pdfminer/pdfminer.six
- https://github.com/gaearon/redux-devtools
