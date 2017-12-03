import graphene

import core.schemaLink, core.schemaIngredient


class Query(core.schemaLink.Query, core.schemaIngredient.Query, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query)
