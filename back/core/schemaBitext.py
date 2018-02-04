import graphene
from graphene_django import DjangoObjectType

from core.models import Bitext, Text, Paragraph, Sentence
from enpc_aligner.dtw import *


class BitextType(DjangoObjectType):
    class Meta:
        model = Bitext

class TextType(DjangoObjectType):
    class Meta:
        model = Text

class ParagraphType(DjangoObjectType):
    class Meta:
        model = Paragraph

class SentenceType(DjangoObjectType):
    class Meta:
        model = Sentence

class Query(object):
    bitext = graphene.Field(BitextType, id=graphene.Int(), name=graphene.String())
    bitexts = graphene.List(BitextType)

    def resolve_bitexts(self, info, **kwargs):
        return Bitext.objects.all()

    def resolve_texts(self, info, **kwargs):
        return Text.objects.select_related('bitext').all()

    def resolve_paragraphs(self, info, **kwargs):
        return Paragraph.objects.select_related('text').all()

    def resolve_sentences(self, info, **kwargs):
        return Sentence.objects.select_related('paragraph').all()

# select_related(*fields)
# renvoie un QuerySet qui « suit » les relations de clé étrangère, sélectionnant
# les données supplémentaires d’éventuels objets liés au moment d’exécuter la requête.
# Il s’agit d’une optimisation en performances qui produit une requête unique plus
# complexe, mais qui évite ensuite de générer de nouvelles requêtes en base de données
# au moment d’accéder aux liaisons de clé étrangère.

    def resolve_bitext(self, info, **kwargs):
        id = kwargs.get('id')
        name = kwargs.get('name')

        if id is not None:
            return Category.objects.get(pk=id)

        if title is not None:
            return Category.objects.get(title=title)

        return None

class CreateBitext(graphene.Mutation):
    id = graphene.Int()
    french = graphene.String()
    english = graphene.String()

    class Arguments:
        french = graphene.String()
        english = graphene.String()

    def mutate(self, info, french, english):
        bitext = Bitext.objects.create()

        fr_original_text, fr_clean_text = parse(french)
        fr_text = Text.objects.create(language="french", bitext=bitext)

        en_original_text, en_clean_text = parse(english)
        en_text = Text.objects.create(language="english", bitext=bitext)

        for id_par, par in enumerate(fr_original_text):
            paragraph = Paragraph.objects.create(id_par=id_par, text=fr_text)
            for id_sen, sen in enumerate(par):
                Sentence.objects.create(id_sen=id_sen, content=sen, paragraph=paragraph)
        for id_par, par in enumerate(en_original_text):
            paragraph = Paragraph.objects.create(id_par=id_par, text=en_text)
            for id_sen, sen in enumerate(par):
                Sentence.objects.create(id_sen=id_sen, content=sen, paragraph=paragraph)

        return CreateBitext(
            id=bitext.id
        )

class Mutation(graphene.ObjectType):
    submit_bitext = CreateBitext.Field()
