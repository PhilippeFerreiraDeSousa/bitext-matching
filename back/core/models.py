# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models


class Bitext(models.Model):
    title = models.CharField(max_length=100, null=True)
    author = models.CharField(max_length=100, null=True)
    creation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Text(models.Model):
    language = models.CharField(max_length=30)
    bitext = models.ForeignKey(Bitext, related_name='texts', on_delete=models.CASCADE)  # enable to call texts: [TextType] as a field of bitext

    def __str__(self):
        return "{} - {}".format(self.bitext.title, self.language)

    @property
    def content(self):
        return "\n\n".join(map(str, Paragraph.objects.filter(text=self)))

class Paragraph(models.Model):
    text = models.ForeignKey(Text, related_name='paragraphs', on_delete=models.CASCADE)  # enable to call paragraphs: [ParagraphType] as a field of text
    id_par = models.IntegerField()

    @property
    def content(self):
        return "\n".join(map(str, Sentence.objects.filter(paragraph=self)))

    def __str__(self):
        return self.content

class Sentence(models.Model):
    content = models.TextField(null=False, blank=False)
    paragraph = models.ForeignKey(Paragraph, related_name='sentences', on_delete=models.CASCADE)  # enable to call sentences: [SentenceType] as a field of paragraph
    id_sen = models.IntegerField()
    #id_sen_in_text = models.IntegerField()

    def __str__(self):
        return self.content

class Word(models.Model):
    content = models.CharField(max_length=30)
    sentence = models.ForeignKey(Sentence, related_name='words', on_delete=models.CASCADE)

    def __str__(self):
        return self.content
