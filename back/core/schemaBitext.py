import graphene
from graphene_django import DjangoObjectType

from core.models import Bitext


class BitextType(DjangoObjectType):
    class Meta:
        model = Bitext


class Query(object):
    bitexts = graphene.List(BitextType)

    def resolve_bitexts(self, info, **kwargs):
        return Bitext.objects.all()

class CreateBitext(graphene.Mutation):
    id = graphene.Int()
    french = graphene.String()
    english = graphene.String()

    class Arguments:
        french = graphene.String()
        english = graphene.String()

    def mutate(self, info, french, english):
        bitext = Bitext(french=french, english=english)
        bitext.save()

        return CreateBitext(
            id=bitext.id,
            french=bitext.french,
            english=bitext.english,
        )

class Mutation(graphene.ObjectType):
    submit_bitext = CreateBitext.Field()
