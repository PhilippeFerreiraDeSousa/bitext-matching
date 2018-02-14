import graphene
from graphene_django import DjangoObjectType
from .paginateHelper import get_paginator

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

class BitextAlignmentInfoType(graphene.ObjectType):
    alignments_number = graphene.Int()
    progress_number = graphene.Int()

class AlignmentPaginatedType(graphene.ObjectType):
    page = graphene.Int()
    pages = graphene.Int()
    has_next = graphene.Boolean()
    has_prev = graphene.Boolean()
    objects = graphene.List(AlignmentType)

class Query(object):
    bitext = graphene.Field(BitextType, id=graphene.Int(), title=graphene.String())
    all_bitexts = graphene.List(BitextType)
    all_words = graphene.List(WordType)
    alignments = graphene.Field(AlignmentPaginatedType, bitext_id=graphene.Int(), page=graphene.Int())
    translations = graphene.List(TranslationType, word_id=graphene.Int(), bitext_id=graphene.Int())
    alignment_info = graphene.Field(BitextAlignmentInfoType, id=graphene.Int())

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

    def resolve_alignment_info(self, info, **kwargs):
        bitext_id = kwargs.get('id')
        print("Bitext id :", bitext_id)
        alignments_number = Bitext.objects.get(id=bitext_id).alignments_number
        print("Alignments Number :", alignments_number)
        progress_number = Alignment.objects.filter(bitext__id=bitext_id).count()
        print("Progress number :", progress_number)

        return BitextAlignmentInfoType(alignments_number=alignments_number, progress_number=progress_number)

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

    def resolve_alignments(self, info, bitext_id=None, page=1, **kwargs):
        alignments = Alignment.objects.filter(bitext__id=bitext_id)
        page_size = 20

        return get_paginator(alignments, page_size, page, AlignmentPaginatedType)
    # Blog.objects.filter(entry__headline__contains='Lennon') sélectionne tous les objets Blog ayant au moins une Entry ayant un headline contenant 'Lennon'

    def resolve_translations(self, info, **kwargs):
        word_id = kwargs.get('word_id')
        bitext_id = kwargs.get('bitext_id')

        if word_id is not None:
            return (Translation.objects.filter(word_1_id=word_id) | Translation.objects.filter(word_2_id=word_id)).order_by('score')

        if bitext_id is not None:
            return Translation.objects.filter(bitext__id=bitext_id)

        return None

class SubmitBitext(graphene.Mutation):
    id = graphene.Int()

    class Arguments:
        title = graphene.String()
        author = graphene.String()

    def mutate(self, info, title, author):
        bitext = Bitext.objects.create(title=title, author=author)

        return SubmitBitext(
            id=bitext.id
        )

class AlignBitext(graphene.Mutation):
    id = graphene.Int()

    class Arguments:
        id = graphene.Int()
        text_1 = graphene.String()
        text_2 = graphene.String()
        language_1 = graphene.String()
        language_2 = graphene.String()

    def mutate(self, info, id, text_1, text_2, language_1, language_2):
        bitext = Bitext.objects.get(id=id)

        original_text_1, clean_text_1 = parse(text_1, language_1)
        text1 = Text.objects.create(language=language_1, bitext=bitext)

        original_text_2, clean_text_2 = parse(text_2, language_2)
        text2 = Text.objects.create(language=language_2, bitext=bitext)

        alignments, matches = align_paragraphs(clean_text_1, clean_text_2)
        matches_1 = matches # sorted on word index in text 1
        matches_2 = sorted(matches, key=lambda x: x[1][3]) # sort on word index in text 2
        bitext.alignments_number = len(alignments)
        for match in matches:
            print(clean_text_1[match[0][0][0]][match[0][0][1]][match[0][0][2]], match[0][0], "|", clean_text_2[match[1][0][0]][match[1][0][1]][match[1][0][2]], match[1][0])
        print(alignments)
        bitext.save()

        match_cursor_1 = 0
        match_cursor_2 = 0
        Words_1 = []
        Sentences_1 = []
        Words_2 = []
        Sentences_2 = []

        for id_alignment, align in enumerate(alignments):
            alignment = Alignment.objects.create(bitext=bitext, id_alignment=id_alignment)
            print("en_alignment :", alignment)
            for id_par_1 in align[0]:
                print("en_par :", id_par_1)
                paragraph = Paragraph.objects.create(id_par=id_par_1, text=text1, alignment=alignment)
                for id_sen, sen in enumerate(original_text_1[id_par_1]):
                    sentence_1 = Sentence.objects.create(id_sen=id_sen, content=sen, paragraph=paragraph)
                    while match_cursor_1 < len(matches_1) and id_par_1 == matches_1[match_cursor_1][0][0][0] and id_sen == matches_1[match_cursor_1][0][0][1]:
                        Q_word_1 = Word.objects.filter(content=clean_text_1[id_par_1][id_sen][matches_1[match_cursor_1][0][0][2]], language=language_1)
                        if Q_word_1:
                            word_1 = list(Q_word_1)[0]
                        else:
                            word_1 = Word.objects.create(content=clean_text_1[id_par_1][id_sen][matches_1[match_cursor_1][0][0][2]], language=language_1)
                        print("en_word", match_cursor_1, ":", word_1.content)
                        print(sentence_1.content)
                        Words_1.append(word_1)
                        Sentences_1.append(sentence_1)
                        if match_cursor_1 < match_cursor_2:
                            Translation.objects.create(bitext=bitext, word_1=Words_1[match_cursor_1], word_2=Words_2[match_cursor_1], sentence_1=Sentences_1[match_cursor_1], sentence_2=Sentences_2[match_cursor_1], score=matches[match_cursor_1][2])
                        match_cursor_1 += 1

            for id_par_2 in align[1]:
                print("fr_par :", id_par_2)
                paragraph = Paragraph.objects.create(id_par=id_par_2, text=text2, alignment=alignment)
                for id_sen, sen in enumerate(original_text_2[id_par_2]):
                    sentence_2 = Sentence.objects.create(id_sen=id_sen, content=sen, paragraph=paragraph)
                    while match_cursor_2 < len(matches_2) and id_par_2 == matches_2[match_cursor_2][1][0][0] and id_sen == matches_2[match_cursor_2][1][0][1]:
                        Q_word_2 = Word.objects.filter(content=clean_text_2[id_par_2][id_sen][matches_2[match_cursor_2][1][0][2]], language=language_2)
                        if Q_word_2:
                            word_2 = list(Q_word_2)[0]
                        else:
                            word_2 = Word.objects.create(content=clean_text_2[id_par_2][id_sen][matches_2[match_cursor_2][1][0][2]], language=language_2)
                        print("fr_word", match_cursor_2, ":", word_2.content)
                        print(sentence_2.content)
                        Words_2.append(word_2)
                        Sentences_2.append(sentence_2)
                        if match_cursor_2 < match_cursor_1:
                            print("Translation", match_cursor_2, ":", Words_1[match_cursor_2], "|", Words_2[match_cursor_2])
                            Translation.objects.create(bitext=bitext, word_1=Words_1[match_cursor_2], word_2=Words_2[match_cursor_2], sentence_1=Sentences_1[match_cursor_2], sentence_2=Sentences_2[match_cursor_2], score=matches[match_cursor_2][2])
                        match_cursor_2 += 1

        return AlignBitext(id=id)

class Mutation(graphene.ObjectType):
    submit_bitext = SubmitBitext.Field()
    align_bitext = AlignBitext.Field()
