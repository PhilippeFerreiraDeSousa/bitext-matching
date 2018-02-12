import graphene

import core.schemaBitext
import core.subscriptions


class Query(core.schemaBitext.Query, graphene.ObjectType):
    pass

class Mutation(core.schemaBitext.Mutation, graphene.ObjectType):
    pass

class RootSubscription(custom.app.route.graphql.schema.Subscriptions, graphene.ObjectType):
    class Meta:
        description = 'The project root subscription definition'

schema = graphene.Schema(
    query=Query,
    mutation=Mutation,
    subscription=RootSubscription
)
