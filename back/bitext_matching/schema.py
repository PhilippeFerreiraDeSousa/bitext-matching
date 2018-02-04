import graphene

import core.schemaBitext


class Query(core.schemaBitext.Query, graphene.ObjectType):
    pass

class Mutation(core.schemaBitext.Mutation, graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)
