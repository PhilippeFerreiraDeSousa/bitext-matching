import graphene
from graphene_django import DjangoObjectType

from core.models import Bitext, Text, Paragraph, Sentence, Alignment, Translation, Word
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

class WordType(DjangoObjectType):
    class Meta:
        model = Word

class TranslationType(DjangoObjectType):
    class Meta:
        model = Translation

class Query(object):
    bitext = graphene.Field(BitextType, id=graphene.Int(), name=graphene.String())
    all_bitexts = graphene.List(BitextType)
    all_words = graphene.List(WordType)
    alignments = graphene.List(AlignmentType, bitext_id=graphene.Int())
    translations = graphene.List(TranslationType, bitext_id=graphene.Int())

    def resolve_all_bitexts(self, info, **kwargs):
        return Bitext.objects.all()

    def resolve_all_words(self, info, **kwargs):
        return Word.objects.all()

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
        title = kwargs.get('title')

        if id is not None:
            return Bitext.objects.get(pk=id)

        if title is not None:
            return Bitext.objects.get(title=title)

        return None

    def resolve_alignments(self, info, **kwargs):
        bitext_id = kwargs.get('bitext_id')
        return Alignment.objects.filter(bitext_id=bitext_id).order_by('id_alignment')   # bitext_id : on peut filtrer sur l'id d'une clef étrangère !

    def resolve_translations(self, info, **kwargs):
        bitext_id = kwargs.get('bitext_id')
        return Translation.objects.filter(bitext_id=bitext_id).order_by('score')

class CreateBitext(graphene.Mutation):
    id = graphene.Int()
    french = graphene.String()
    english = graphene.String()
    title = graphene.String()
    author = graphene.String()

    class Arguments:
        french = graphene.String()
        english = graphene.String()
        title = graphene.String()
        author = graphene.String()

    def mutate(self, info, french, english, title, author):
        bitext = Bitext.objects.create(title=title, author=author)

        en_original_text, en_clean_text = parse(english, "en")
        en_text = Text.objects.create(language="english", bitext=bitext)

        fr_original_text, fr_clean_text = parse(french, "fr")
        fr_text = Text.objects.create(language="french", bitext=bitext)

        alignments, matches = align_paragraphs(en_clean_text, fr_clean_text)
        for id_alignment, align in enumerate(alignments):
            alignment = Alignment.objects.create(bitext=bitext, id_alignment=id_alignment)
            for en_id_par in align[0]:
                print(en_id_par)
                paragraph = Paragraph.objects.create(id_par=en_id_par, text=en_text, alignment=alignment)
                for id_sen, sen in enumerate(en_original_text[en_id_par]):
                    Sentence.objects.create(id_sen=id_sen, text=sen, paragraph=paragraph)
            for fr_id_par in align[1]:
                print(fr_id_par)
                paragraph = Paragraph.objects.create(id_par=fr_id_par, text=fr_text, alignment=alignment)
                for id_sen, sen in enumerate(fr_original_text[fr_id_par]):
                    Sentence.objects.create(id_sen=id_sen, text=sen, paragraph=paragraph)

        return CreateBitext(
            id=bitext.id
        )
        #for match in matches:
        #    word_1 = Word.objects.get(text=match[0][0])
        #    if not word_1:
        #        word_1 = Word.objects.create(text=match[0][0], language="english")
        #    word_1.sentences.add()

        #    word_2 = Word.objects.get(text=match[1][0])
        #    if not word_2:
        #        word_2 = Word.objects.create(text=match[1][0], language="french")
        #    word_2.sentences.add()
        #    Translation.objects.create(bitext=bitext, word_1=word_1, word_2=word_2, score=match[2])

class Mutation(graphene.ObjectType):
    submit_bitext = CreateBitext.Field()
