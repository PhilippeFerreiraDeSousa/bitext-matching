# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models


class Bitext(models.Model):
    title = models.CharField(max_length=100, null=True)
    author = models.CharField(max_length=100, null=True)
    creation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title if self.title else "Sans titre"

    class Meta:
        ordering = ['creation_date']

class Text(models.Model):
    language = models.CharField(max_length=30)
    bitext = models.ForeignKey(Bitext, related_name='texts', on_delete=models.CASCADE)  # enable to call texts: [TextType] as a field of bitext

    def __str__(self):
        return "{} - {}".format(self.bitext.title, self.language)

    @property
    def content(self):
        return "\n".join(map(str, Paragraph.objects.filter(text=self)))

class Alignment(models.Model):
    bitext = models.ForeignKey(Bitext, related_name='alignments', on_delete=models.CASCADE)
    id_alignment = models.IntegerField()

    def __str__(self):
        return "{} - {}".format(self.bitext.title, self.id_alignment)

    @property
    def content(self):
        return "\n".join(map(str, Paragraph.objects.filter(alignment=self)))

    class Meta:
        ordering = ['id_alignment']

class Paragraph(models.Model):
    text = models.ForeignKey(Text, related_name='paragraphs', on_delete=models.CASCADE)  # enable to call paragraphs: [ParagraphType] as a field of text
    id_par = models.IntegerField()
    alignment = models.ForeignKey(Alignment, related_name='paragraphs', on_delete=models.CASCADE, null=True)

    @property
    def content(self):
        return " ".join(map(str, Sentence.objects.filter(paragraph=self).order_by('id_sen')))

    def __str__(self):
        return self.content

    class Meta:
        ordering = ['id_par']

class Sentence(models.Model):
    content = models.TextField(null=False, blank=False)
    paragraph = models.ForeignKey(Paragraph, related_name='sentences', on_delete=models.CASCADE)  # enable to call sentences: [SentenceType] as a field of paragraph
    id_sen = models.IntegerField()

    def __str__(self):
        return self.content

    class Meta:
        ordering = ['id_sen']

class Word(models.Model):
    content = models.CharField(max_length=30)
    language = models.CharField(max_length=30)

    def __str__(self):
        return self.content

class Translation(models.Model):
    bitext = models.ForeignKey(Bitext, related_name='translations', on_delete=models.CASCADE)
    word_1 = models.ForeignKey(Word, related_name='translations_1', on_delete=models.CASCADE)
    word_2 = models.ForeignKey(Word, related_name='translations_2', on_delete=models.CASCADE)
    sentence_1 = models.ForeignKey(Sentence, related_name='sentences_1', on_delete=models.CASCADE)
    sentence_2 = models.ForeignKey(Sentence, related_name='sentences_2', on_delete=models.CASCADE)
    score = models.IntegerField()

    def __str__(self):
        return "{} - {} | {} ({})".format(self.bitext.title, self.word_1, self.word_2, self.score)
