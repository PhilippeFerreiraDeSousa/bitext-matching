import graphene
from graphene_django import DjangoObjectType

from core.models import Link


class LinkType(DjangoObjectType):
    class Meta:
        model = Link


class Query(graphene.AbstractType):
    links = graphene.List(LinkType)

    @graphene.resolve_only_args
    def resolve_links(self):
        return Link.objects.all()
