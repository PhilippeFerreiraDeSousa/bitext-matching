import graphene

import core.schemaLink, core.schemaIngredient


class Query(core.schemaLink.Query, core.schemaIngredient.Query, graphene.ObjectType):
    pass

class Mutation(core.schemaLink.Mutation, graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)
