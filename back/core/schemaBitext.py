import graphene
from graphene_django import DjangoObjectType

from core.models import Bitext, Text, Paragraph, Sentence, Alignment
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

class AlignmentType(DjangoObjectType):
    class Meta:
        model = Alignment

class Query(object):
    bitext = graphene.Field(BitextType, id=graphene.Int(), name=graphene.String())
    all_bitexts = graphene.List(BitextType)
    alignments = graphene.List(AlignmentType, bitext_id=graphene.Int())

    def resolve_all_bitexts(self, info, **kwargs):
        return Bitext.objects.all()

    def resolve_texts(self, info, **kwargs):
        return Text.objects.select_related('bitext').all()

    def resolve_paragraphs(self, info, **kwargs):
        return Paragraph.objects.select_related('text').select_related('alignment').all().order_by('id_par')

    def resolve_sentences(self, info, **kwargs):
        return Sentence.objects.select_related('paragraph').all().order_by('id_sen')

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

    def resolve_alignments(self, info, **kwargs):
        bitext_id = kwargs.get('bitext_id')
        return Alignment.objects.filter(bitext_id=bitext_id).order_by('id_alignment')   # bitext_id : on peut filtrer sur l'id d'une clef étrangère !

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

        alignments, translations = align_paragraphs(en_clean_text, fr_clean_text)
        for id_alignment, alignment in enumerate(alignments):
            Alignment.objects.create(bitext=bitext, id_alignment=id_alignment)
            for en_id_par in alignment[0]:
                paragraph = Paragraph.objects.create(id_par=en_id_par, text=en_text)
                for id_sen, sen in enumerate(en_original_text[en_id_par]):
                    Sentence.objects.create(id_sen=id_sen, content=sen, paragraph=paragraph)
            for fr_id_par in alignment[1]:
                paragraph = Paragraph.objects.create(id_par=fr_id_par, text=fr_text)
                for id_sen, sen in enumerate(fr_original_text[fr_id_par]):
                    Sentence.objects.create(id_sen=id_sen, content=sen, paragraph=paragraph)

        return CreateBitext(
            id=bitext.id
        )

class Mutation(graphene.ObjectType):
    submit_bitext = CreateBitext.Field()
