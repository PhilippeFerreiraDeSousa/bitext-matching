import graphene

import core.schemaBitext, core.schemaIngredient


class Query(core.schemaBitext.Query, core.schemaIngredient.Query, graphene.ObjectType):
    pass

class Mutation(core.schemaBitext.Mutation, graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)
